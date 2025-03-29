import asyncio
import time

from . import config
from .metrics import get_load, get_temp, metrics

update_map = {
    "load": get_load,
    "temp": get_temp,
}


async def update_metrics():
    while True:
        now = time.time() * 1000  # javascript expects millisecond precision
        for name, fetch in update_map.items():
            metrics[name].append({"time": now, "value": fetch()})
        await asyncio.sleep(config.TICK_DURATION_S)
