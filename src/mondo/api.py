import asyncio
import typing as t

from quart import Blueprint, websocket

from . import config, metrics

bp = Blueprint("metrics", __name__, url_prefix="/metrics")


def websocket_stream(name: str):
    """A wrapper for streaming metrics over websockets"""

    values = metrics.store[name]

    async def inner():
        try:
            while True:
                await websocket.send_json(values[len(values) - 1])
                await asyncio.sleep(config.TICK_DURATION_S)
        except asyncio.CancelledError:
            pass  # TODO maybe log something?

    return inner


def http_route(name: str):
    """A wrapper for retrieving metrics via http"""

    values = metrics.store[name]

    async def inner():
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
