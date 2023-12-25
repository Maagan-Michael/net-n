import docker
import os
from ..logger import get_logger
from ..config import AppConfig

logger = get_logger("syncModuleJob")


async def toggleSyncModule():
    """start the sync module throught docker"""
    logger.info("starting job")
    try:
        client = docker.from_env()
        container = client.containers.get(AppConfig["sync"]["container"])
        container.environment["CONFIG_PATH"] = os.environ["CONFIG_PATH"]
        container.start()
        logger.info("sync module started throught docker")
    except Exception as e:
        logger.error(e)
        logger.error(f"failed to finish job")
