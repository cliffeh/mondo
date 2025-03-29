import asyncio
import typing as t

from quart import Blueprint, websocket

from . import config, metrics

bp = Blueprint("metrics", __name__, url_prefix="/metrics")


def websocket_stream(fetch: t.Callable):
    """A wrapper for streaming metrics over websockets"""

    async def inner():
        try:
            while True:
                await websocket.send_json(fetch())
                await asyncio.sleep(config.TICK_DURATION_S)
        except asyncio.CancelledError:
            pass  # TODO maybe log something?

    return inner


for name, fetch in metrics.metrics.items():
    rule = f"/{name}"
    bp.add_url_rule(rule, name, fetch)
    bp.add_websocket(rule, f"{name}_ws", websocket_stream(fetch))


@bp.route("")
def get_metrics() -> dict[str, dict[str, float]]:
    """Get all metrics"""
    return {name: fetch() for name, fetch in metrics.metrics.items()}
