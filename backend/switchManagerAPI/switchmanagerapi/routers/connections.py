from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Union
from ..adapters.sync import AppAdapter
from sqlalchemy import Column, asc, desc, or_, select, and_, update
from sqlalchemy.orm import contains_eager
from ..models import BatchedDeleteOutput, OrderBy, Connection, AssignCustomerInput, \
    BatchConnectionOutput, ConnectionOutput, ConnectionsOutput, ConnectionListInput, ConnectionUpsertInput, ListFilterEnum, ListSortEnum
from ..db import DBConnection, DBSwitch, DBCustomer, ConnectionRepository
import re
from ..logger import get_logger

logger = get_logger("ConnectionRouter")

router = APIRouter(
    tags=["v1", "connections"],
    prefix="/api/v1/connections",
    responses={404: {"description": "Not found"}},
)

# connections CRUD
# map API sort enum to database indexed columns
sortEnumMap: dict[ListSortEnum, List[Column[any]]] = {
    ListSortEnum.con: [DBConnection.name],
    ListSortEnum.customerId: [DBConnection.customerId],
    ListSortEnum.address: [DBConnection.address],
    ListSortEnum.fullname: [DBCustomer.lastname, DBCustomer.firstname],
    ListSortEnum.switch: [DBSwitch.name],
}


def getFilterStm(search: Optional[str], filter: ListFilterEnum):
    """return a list of filters for a given search and filter"""
    filters = []
    # status filters
    if (filter == ListFilterEnum.enabled):
        filters.append(DBConnection.toggled == True)
    elif (filter == ListFilterEnum.disabled):
        filters.append(DBConnection.toggled == False)
    elif (filter == ListFilterEnum.up):
        filters.append(DBConnection.isUp == True)
    elif (filter == ListFilterEnum.down):
        filters.append(DBConnection.isUp == False)

    if (search and len(search) > 0):
        search = [re.escape(e) for e in search.strip().split(" ")]
        wc = len(search)
        isMultiWord = wc > 1
        orSearch = "(^|{\s}?)" + \
            f"({'|'.join(search)}).*" if wc > 1 else f".*{search[0]}.*"
        andSearch = f".*{'.*'.join(search)}.*"
        if (filter == ListFilterEnum.customerId):
            filters.append(DBCustomer.idstr.op('~*')(orSearch))
        elif (filter == ListFilterEnum.address):
            filters.append(DBConnection.address.op('~*')(andSearch))
        elif (filter == ListFilterEnum.port):
            filters.append(DBConnection.strPort.op('~*')(orSearch))
        elif (filter == ListFilterEnum.switch):
            filters.append(DBSwitch.name.op('~*')(orSearch))
        else:
            if (filter == ListFilterEnum.customer):
                operator = and_ if isMultiWord else or_
                filters.append(
                    operator(
                        DBCustomer.firstname.op('~*')(orSearch),
                        DBCustomer.lastname.op('~*')(orSearch),
                    )
                )
            elif (isMultiWord):
                # general search
                filters.append(
                    or_(
                        and_(
                            DBCustomer.firstname.op('~*')(orSearch),
                            DBCustomer.lastname.op('~*')(orSearch),
                        ),
                        DBConnection.address.op('~*')(andSearch),
                        and_(
                            DBSwitch.name.op('~*')(orSearch),
                            DBConnection.strPort.op('~*')(orSearch),
                        )
                    )
                )
            else:
                filters.append(or_(
                    DBConnection.name.op('~*')(orSearch),
                    DBCustomer.idstr.op('~*')(orSearch),
                    DBConnection.strPort.op('~*')(orSearch),
                    # todo handle spaces in orSearch for firstname + lastname
                    DBCustomer.firstname.op('~*')(orSearch),
                    DBCustomer.lastname.op('~*')(orSearch),
                    DBConnection.address.op('~*')(andSearch),
                    DBSwitch.name.op('~*')(orSearch),
                ))
    return filters


@router.get("/", response_model=ConnectionsOutput)
async def listConnections(repo: ConnectionRepository, input: ConnectionListInput = Depends()):
    """return a paginated list of connections"""
    filters = getFilterStm(input.search, input.filter)
    obFields = sortEnumMap[input.sort]
    orderBy = [desc(e) for e in obFields] if input.order == OrderBy.desc else [
        asc(e) for e in obFields]
    print(*orderBy)
    stm = (
        select(DBConnection)
        .join(DBConnection.customer, isouter=True)
        .join(DBConnection.switch)
        .options(contains_eager(DBConnection.customer), contains_eager(DBConnection.switch))
        .order_by(*orderBy)
        .filter(*filters)
        .offset(input.page * input.limit)
        .limit(input.limit + 1)
        .execution_options(populate_existing=True)
    )
    q = await repo.session.scalars(stm)
    # todo : compute hasPrevious (not needed as of now)
    res = []
    for (idx, e) in enumerate(q):
        connection = ConnectionOutput.model_construct(**e.__dict__)
        res.insert(idx, connection)
    hasPrevious = input.page > 0
    hasNext = len(res) > input.limit
    if (hasNext):
        res.pop()
    return ConnectionsOutput(
        connections=res,
        hasNext=hasNext,
        hasPrevious=hasPrevious,
    )


@router.get("/{id}", response_model=ConnectionOutput)
async def getConnection(id: str, repo: ConnectionRepository):
    """return a connection by id"""
    q = await repo.session.scalar(
        select(DBConnection)
        .join(DBConnection.customer, isouter=True)
        .join(DBConnection.switch)
        .options(contains_eager(DBConnection.customer), contains_eager(DBConnection.switch))
        .where(DBConnection.id == id)
        .execution_options(populate_existing=True)
        .limit(1)
    )
    if q is not None:
        return ConnectionOutput.model_construct(**q.__dict__)
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/assign", response_model=ConnectionOutput)
async def assignConnectionCustomer(input: AssignCustomerInput, repo: ConnectionRepository):
    """
        assign a connection to a customer by address and flat
    """
    customer = await repo.session.scalar(
        select(DBCustomer).where(DBCustomer.id == input.customerId)
    )
    if (customer is None):
        raise HTTPException(
            status_code=404, detail="Customer not found")
    connection = None
    if (input.connectionId):
        connection = await repo.session.scalar(
            select(DBConnection).where(DBConnection.id == input.connectionId)
        )
    if (input.address):
        connection = await repo.session.scalar(
            select(DBConnection).where(
                DBConnection.address == input.address and
                DBConnection.flat == input.flat
            )
            .join(DBConnection.customer, isouter=True)
            .join(DBConnection.switch)
            .options(contains_eager(DBConnection.customer), contains_eager(DBConnection.switch))
            .execution_options(populate_existing=True)
        )
    if (connection is None):
        raise HTTPException(
            status_code=404, detail="Connection not found")
    logger.warning(
        f"assigning connection {connection.id} to customer {customer.id}")
    if (connection.customerId != customer.id):
        logger.warning(
            f"replacing old customer {connection.customerId} with {customer.id}")
    connection.customerId = customer.id
    return ConnectionOutput.model_construct(**connection.__dict__)


@router.post("/upsert", response_model=BatchConnectionOutput)
async def upsertConnection(input: Union[ConnectionUpsertInput, list[ConnectionUpsertInput]], repo: ConnectionRepository):
    """
        upsert or udpate one || multiple connections
        handle side effects :
            - toggle connection with newtork adapter
            - close old port with network adapter if port changed
            - logs changes and events (customer, port, toggled, restricted)
        TODO: if a customer is assigned to a connection, he should be removed from other connections (if autoUpdate is true) and the said connection
              should be closed with the adapter
    """
    [items, errors, previousValues] = await repo.batch_upsert(input)
    ids = [e.id for e in items]
    items = (await repo.session.scalars(
        select(DBConnection)
        .join(DBConnection.customer, isouter=True)
        .join(DBConnection.switch)
        .options(contains_eager(DBConnection.customer), contains_eager(DBConnection.switch))
        .where(DBConnection.id.in_(ids))
        .execution_options(populate_existing=True)
    )).all()
    for (idx, e) in enumerate(previousValues):
        if e:
            items[idx] = ConnectionOutput.model_construct(
                **items[idx].__dict__)
            b = items[idx]
            try:
                # customer changed : log the change
                if (e.customerId != b.customerId):
                    logger.warning(
                        f"customer changed on connection ({b.name})({b.id}) from {e.customerId} to {b.customerId}")
                #   - if the customer is null, then close the connection with the adapter (if autoUpdate is true)
                if (b.customerId is None and b.autoUpdate and b.toggled):
                    await repo.session.execute(
                        update(DBConnection)
                        .where(DBConnection.id == b.id)
                        .values(toggled=False)
                    )
                    b.toggled = False
                    logger.warning(
                        f"closing connection {b.id} on {b.switch.name}({b.switch.ip}:{b.port})")
                    AppAdapter.adapter.togglePort(
                        b.switch.ip, b.port, False)
                # toggled changed :
                #   - log the change
                #   - toggle connection with adapter
                if (e.toggled != b.toggled):
                    logger.info(
                        f"toggling {'on' if b.toggled else 'off'} connection {b.id} on {b.switch.name}({b.switch.ip}:{b.port})")
                    AppAdapter.adapter.togglePort(
                        b.switch.ip, b.port, b.toggled)
                # port changed :
                #   - log the change
                #   - toggle connection with adapter
                #   - close old port with adapter
                if (e.port != b.port):
                    # closing old port with adapter
                    logger.info(
                        f"port changed on connection ({b.name})({b.id}) closing old port {e.port}")
                    AppAdapter.adapter.togglePort(
                        b.switch.ip, b.port, b.toggled)
                    AppAdapter.adapter.togglePort(
                        b.switch.ip, e.port, False)
                # connection was upserted by is using a restricted port or restricted switch (log the changes)
                if (b.port in b.switch.restrictedPorts):
                    logger.error(
                        f"the connection:{b.name} with the restricted port {b.port} on switch:{b.switch.name} was modified")
                if (b.switch.restricted):
                    logger.error(
                        f"The connection:{b.name} on the restricted switch:{b.switch.name} connection was modified")
            except Exception as ex:
                logger.error(ex)
                raise Exception(
                    f"network op failed for {b.switch.ip}:{b.port}")
    return BatchConnectionOutput.model_construct(items=items, errors=errors)


@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteConnection(ids: list[str], repo: ConnectionRepository):
    """delete a connection"""
    return repo.delete(ids)
