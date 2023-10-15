import uvicorn
from fastapi import FastAPI, Depends
from .io import *

app = FastAPI()

@app.get("/api/list")
async def list_connections(input: ConnectionListInput = Depends()) -> ConnectionsOutput:
    """return a paginated list of connections"""
    return ConnectionsOutput()

def main():
    """Run the API server"""
    uvicorn.run("switchmanagerapi.main:app", host="0.0.0.0", port=8000, reload=True)