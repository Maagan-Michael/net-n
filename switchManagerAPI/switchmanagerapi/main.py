import uvicorn
from fastapi import FastAPI, Depends
from .io import *

app = FastAPI(
    # todo : authentification dependency with external oauth service
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@app.get("/api/v1/connections", tags=["v1"], response_model=ConnectionsOutput)
async def listConnections(input: ConnectionListInput = Depends()) -> ConnectionsOutput:
    """return a paginated list of connections"""
    return ConnectionsOutput()

@app.post("/api/v1/connection", tags=["v1"], response_model=ConnectionOutput)
async def updateConnection(input: ConnectionInput) -> ConnectionOutput:
    """update a connection"""
    return ConnectionOutput()

def main():
    """Run the API server"""
    uvicorn.run("switchmanagerapi.main:app", host="0.0.0.0", port=8000, reload=True)