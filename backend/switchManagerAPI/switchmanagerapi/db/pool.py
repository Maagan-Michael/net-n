from sqlalchemy.pool import QueuePool
import psycopg2
from ..config import AppConfig


def connect():
    return psycopg2.connect(
        user=AppConfig["db"]["user"],
        password=AppConfig["db"]["password"],
        host=AppConfig["db"]["host"],
        port=AppConfig["db"]["port"],
        database=AppConfig["db"]["database"]
    )


DbPool = QueuePool(connect)
