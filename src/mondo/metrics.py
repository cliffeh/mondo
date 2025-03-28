import asyncio
import os
import typing as t
from functools import wraps
from quart import Blueprint, request, websocket

from . import config

bp = Blueprint("metrics", __name__, url_prefix="/metrics")


def websocket_stream(fetch: t.Callable):
    async def inner():
        try:
            while True:
                await websocket.send_json(fetch())
                await asyncio.sleep(config.TICK_DURATION_S)
        except asyncio.CancelledError:
            # Handle disconnection here
            pass  # TODO maybe log something?

    return inner


@bp.route("")
def get_metrics() -> dict[str, dict[str, float]]:
    return {"load": get_load(), "temp": get_temp()}


bp.add_websocket("", "get_metrics_ws", websocket_stream(get_metrics))


@bp.route("/load")
def get_load() -> dict[str, float]:
    """Get system load average"""
    la = os.getloadavg()
    return {"1m": la[0], "5m": la[1], "15m": la[2]}


bp.add_websocket("/load", "get_load_ws", websocket_stream(get_load))


@bp.route("/temp")
def get_temp() -> dict[str, float]:
    """Get system temperature sensor values"""
    i = 0
    temps = {}
    while True:
        try:
            with open(f"/sys/class/thermal/thermal_zone{i}/type") as typefile, open(
                f"/sys/class/thermal/thermal_zone{i}/temp"
            ) as tempfile:
                temps[typefile.read().strip().replace(" ", "-")] = (
                    float(tempfile.read().strip()) / 1000.0
                )
            i += 1
        except FileNotFoundError:
            return temps


bp.add_websocket("/temp", "get_temp_ws", websocket_stream(get_temp))
