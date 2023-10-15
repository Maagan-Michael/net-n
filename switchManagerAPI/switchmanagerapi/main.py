import uvicorn
from fastapi import FastAPI, Depends
from .io import *

app = FastAPI(
    # todo : authentification dependency with external oauth service
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

# connections CRUD
@app.get("/api/v1/connections", tags=["v1"], response_model=ConnectionsOutput)
async def listConnections(input: ConnectionListInput = Depends()) -> ConnectionsOutput:
    """return a paginated list of connections"""
    return ConnectionsOutput()

@app.get("/api/v1/connection/{id}", tags=["v1"], response_model=ConnectionOutput)
async def getConnection(id: int) -> ConnectionOutput:
    """return a connection"""
    return ConnectionOutput()

@app.post("/api/v1/connection/create", tags=["v1"], response_model=ConnectionOutput)
async def createConnection(input: ConnectionInput) -> ConnectionOutput:
    """create a connection"""
    return ConnectionOutput()

@app.post("/api/v1/connection/update/{id}", tags=["v1"], response_model=ConnectionOutput)
async def updateConnection(input: UpdateConnectionInput) -> ConnectionOutput:
    """update a connection"""
    return ConnectionOutput()

@app.delete("/api/v1/connection/delete/{id}", tags=["v1"], response_model=str)
async def deleteConnection(id: int) -> str:
    """delete a connection"""
    return id

# switches CRUD
@app.get("/api/v1/switches", tags=["v1"], response_model=list[Switch])
async def listSwitches() -> list[Switch]:
    """return a list of switches"""
    return []

@app.get("/api/v1/switch/{id}", tags=["v1"], response_model=Switch)
async def getSwitch(id: int) -> Switch:
    """return a switch"""
    return Switch()

@app.post("/api/v1/switch/create", tags=["v1"], response_model=Switch)
async def createSwitch(input: Switch) -> Switch:
    """create a switch"""
    return Switch()

@app.post("/api/v1/switch/update/{id}", tags=["v1"], response_model=Switch)
async def updateSwitch(input: Switch) -> Switch:
    """update a switch"""
    return Switch()

@app.delete("/api/v1/switch/delete/{id}", tags=["v1"], response_model=str)
async def deleteSwitch(id: int) -> str:
    """delete a switch"""
    return id

# customers CRUD
@app.get("/api/v1/customers", tags=["v1"], response_model=list[Customer])
async def listCustomers() -> list[Customer]:
    """return a list of customers"""
    return []

@app.get("/api/v1/customer/{id}", tags=["v1"], response_model=Customer)
async def getCustomer(id: int) -> Customer:
    """return a customer"""
    return Customer()

@app.post("/api/v1/customer/create", tags=["v1"], response_model=Customer)
async def createCustomer(input: Customer) -> Customer:
    """create a customer"""
    return Customer()

@app.post("/api/v1/customer/update/{id}", tags=["v1"], response_model=Customer)
async def updateCustomer(input: Customer) -> Customer:
    """update a customer"""
    return Customer()

@app.delete("/api/v1/customer/delete/{id}", tags=["v1"], response_model=str)
async def deleteCustomer(id: int) -> str:
    """delete a customer"""
    return id

def main():
    """Run the API server"""
    uvicorn.run("switchmanagerapi.main:app", host="0.0.0.0", port=8000, reload=True)