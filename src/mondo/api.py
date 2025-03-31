import asyncio
import typing as t

from quart import Blueprint, websocket

from . import config, metrics, tasks

bp = Blueprint("metrics", __name__, url_prefix="/metrics")


def websocket_stream(name: str):
    """A wrapper for streaming metrics over websockets"""

    async def inner():
        queue = asyncio.Queue()
        tasks.ws_queues[name].append(queue)
        try:
            while True:
                value = await queue.get()
                await websocket.send_json(value)
        except asyncio.CancelledError:
            tasks.ws_queues[name].remove(queue)

    return inner


def http_route(name: str):
    """A wrapper for retrieving metrics via http"""

    async def inner():
        values = metrics.store[name]
        return values[len(values) - 1]

    return inner


ENABLED_ROUTES = {name: http_route(name) for name in config.ENABLED_METRICS}

for name in config.ENABLED_METRICS:
    rule = f"/{name}"
    bp.add_url_rule(rule, name, ENABLED_ROUTES[name])
    bp.add_websocket(rule, f"{name}_ws", websocket_stream(name))


@bp.route("")
async def get_metrics() -> dict[str, dict[str, float]]:
    """Get all metrics"""
    return {name: await ENABLED_ROUTES[name]() for name in ENABLED_ROUTES}
