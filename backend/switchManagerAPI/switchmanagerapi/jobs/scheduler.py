# uncompatible with pydantic 2
# from rocketry import Rocketry
# scheduler = Rocketry()

import asyncio


async def schedule_every(timeout, stuff):
    """schedule a coroutine every x seconds"""
    while True:
        await asyncio.sleep(timeout)
        await stuff()
