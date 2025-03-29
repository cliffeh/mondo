import os
from collections import deque
import typing as t
from . import config


def load() -> dict[str, float]:
    """Get system load average"""
    la = os.getloadavg()
    return {"1m": la[0], "5m": la[1], "15m": la[2]}


def temp() -> dict[str, float]:
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


metrics: dict[str, t.Callable] = {
    "load": load,
    "temp": temp,
}
store: dict[str, deque[dict[float, float]]] = {
    name: deque([], maxlen=config.MAX_POINTS) for name in metrics.keys()
}
