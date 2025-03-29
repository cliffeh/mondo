import asyncio
import time

from . import config
from .metrics import metrics, store


async def update_metrics():
    while True:
        now = time.time() * 1000  # javascript expects millisecond precision
        for name, fetch in metrics.items():
            store[name].append({"time": now, "value": fetch()})
        await asyncio.sleep(config.TICK_DURATION_S)
