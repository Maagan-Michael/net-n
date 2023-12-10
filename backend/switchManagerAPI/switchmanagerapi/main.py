import os
import time
import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from switchmanagerapi.routers import connections, customers, switches
from .tests.mockups import generateMockupDB
from .db.context import create_db, drop_db
from .adapters.sync import AppAdapter
from .jobs.connections import toggleDueConnections
from .jobs.scheduler import schedule_every

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

jobs = []


@app.on_event("shutdown")
async def on_shutdown():
    """
    Run on shutdown
    - cancel all running background jobs
    """
    for job in jobs:
        if (not job.cancelled() and not job.done()):
            job.cancel()


@app.on_event("startup")
async def on_startup():
    """
        Run on startup
        - create database
        - start network adapter sync on startup
        - start network adapter sync every 24 hours
        - checks for due connections on startup
        - checks for due connections every 12 hours
    """

    # drop database (for testing purposes)
    # await drop_db()

    # create database
    await create_db()

    # generate mockup database (for testing purposes)
    # await generateMockupDB()

    # start network adapter sync on startup
    jobs.append(asyncio.create_task(AppAdapter.sync()))
    # start network adapter sync every 24 hours
    jobs.append(asyncio.create_task(
        schedule_every(60 * 60 * 24, AppAdapter.sync))
    )
    # checks for due connections on startup
    jobs.append(asyncio.create_task(toggleDueConnections()))
    # checks for due connections every 12 hours
    jobs.append(asyncio.create_task(
        schedule_every(60 * 60 * 12, toggleDueConnections)))


def main():
    """
        Run the API server
        this is the entrypoint of the application when running in development
        for production, run "uvicorn switchmanagerapi.main:app --host IP --port PORT"
    """
    uvicorn.run("switchmanagerapi.main:app",
                host="0.0.0.0", port=8000, reload=True)
