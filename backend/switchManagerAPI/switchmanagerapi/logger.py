import sys
from loguru import logger


def get_logger(module: str) -> type[logger]:
    logger.remove()
    logger.add(sys.stdout, colorize=True,
               format="{level}:\t  <g>{time:YYYY-MM-DD:HH:mm:ss}</g> | <y>{extra[module]}</y> | <level>{message}</level>")
    return logger.bind(module=module)
