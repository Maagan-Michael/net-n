import uvicorn
from fastapi import FastAPI
from switchmanagerapi.routers import connections, customers, switches


app = FastAPI(
    # todo : authentification dependency with external oauth service
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

app.include_router(connections.router)
app.include_router(customers.router)
app.include_router(switches.router)

def main():
    """Run the API server"""
    uvicorn.run("switchmanagerapi.main:app", host="0.0.0.0", port=8000, reload=True)