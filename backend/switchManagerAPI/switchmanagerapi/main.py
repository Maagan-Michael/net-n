import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from switchmanagerapi.routers import connections, customers, switches
from .db import create_db

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
    await create_db()


def main():
    """Run the API server"""
    uvicorn.run("switchmanagerapi.main:app",
                host="0.0.0.0", port=8000, reload=True)
