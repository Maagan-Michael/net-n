from sqlalchemy import select
import datetime
from ..db.schemas import DBConnection
from ..db.context import get_context_db_session
from ..logger import get_logger

logger = get_logger("ConnectionJob")


async def toggleDueConnections():
    """toggle connections that are due (toggleDate)"""
    time = datetime.datetime.now()
    logger.info("starting job")
    try:
        async with get_context_db_session() as session:
            # toggle connections that are due
            cons = (await session.scalars(
                select(DBConnection)
                .where(DBConnection.toggleDate <= time)
            )).all()
            for con in cons:
                con.toggled = not con.toggled
                logger.info(
                    f"connection:{con.id} is due for {con.toggleDate}, {'enabling' if con.toggled else 'disabling'} now")
                con.toggleDate = None
                session.add(con)
            logger.info(
                f"{len(cons)} connections impacted")
    except Exception as e:
        logger.error(e)
        logger.error(f"failed to finish job")
