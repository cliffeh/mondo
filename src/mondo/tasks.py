import asyncio
import time

from . import config, metrics


ws_queues: dict[str, list[asyncio.Queue]] = {
    name: [] for name in config.ENABLED_METRICS
}


async def update_metrics():
    """Updates stored metrics and enqueues the latest values to be consumed by
    websocket clients"""
    while True:
        now = time.time()
        for name in config.ENABLED_METRICS:
            # NB javascript expects millisecond precision
            value = {"time": now * 1000, "values": metrics.ALL_METRICS[name]()}
            metrics.store[name].append(value)
            for queue in ws_queues[name]:
                try:
                    await queue.put(value)
                except asyncio.QueueShutDown:
                    ws_queues[name].remove(queue)

        elapsed = time.time() - now
        if elapsed < config.TICK_DURATION_S:
            await asyncio.sleep(config.TICK_DURATION_S - elapsed)
