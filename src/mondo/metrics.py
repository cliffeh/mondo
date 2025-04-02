import os
from collections import deque

from . import config

# ring buffer for storing the last MAX_POINTS values
store: dict[str, deque[dict[str, dict[str, float]]]] = {
    name: deque([], maxlen=config.MAX_POINTS) for name in config.ENABLED_METRICS
}


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


"""map of metric name => collection function"""
ALL_METRICS = {
    "load": load,
    "temp": temp,
}
