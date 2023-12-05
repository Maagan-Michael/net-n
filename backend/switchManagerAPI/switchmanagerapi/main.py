import os
import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from switchmanagerapi.routers import connections, customers, switches
from .tests.mockups import generateMockupDB
from .db.context import create_db, drop_db
from .adapters.sync import AdapterSyncModule

origins = [
    "http://localhost:3000",
]

app = FastAPI(
    # todo : authentification dependency with external oauth service
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(connections.router)
app.include_router(customers.router)
app.include_router(switches.router)


@app.on_event("startup")
async def on_startup():
    """Run on startup"""
    # pass
    # await generateMockupDB()
    # await drop_db()
    # await create_db()
    # module = AdapterSyncModule()
    # print(module.adapter.getSwitchInterface("172.22.10.2", 630))
    # print(module.adapter.getSwitchInterface("10.100.64.251", 165))
    # print(module.adapter.getSwitchInterface("10.100.65.251", 702))
    # module.sync()


def main():
    """Run the API server"""
    uvicorn.run("switchmanagerapi.main:app",
                host="0.0.0.0", port=8000, reload=True)
