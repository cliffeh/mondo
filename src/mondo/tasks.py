import asyncio
import time

from . import config, metrics


async def update_metrics():
    while True:
        now = time.time() * 1000  # javascript expects millisecond precision
        for name in config.ENABLED_METRICS:
            metrics.store[name].append(
                {"time": now, "values": metrics.ALL_METRICS[name]()}
            )
        await asyncio.sleep(config.TICK_DURATION_S)
