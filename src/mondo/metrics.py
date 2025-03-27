import os
from quart import Blueprint

bp = Blueprint("metrics", __name__, url_prefix="/metrics")


@bp.route("")
def get_metrics() -> dict[str, dict[str, float]]:
    return {"load": get_load(), "temp": get_temp()}


@bp.route("/load")
def get_load() -> dict[str, float]:
    """Get system load average"""
    la = os.getloadavg()
    return {"1m": la[0], "5m": la[1], "15m": la[2]}


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
                temps[typefile.read().strip()] = float(tempfile.read().strip()) / 1000.0
            i += 1
        except FileNotFoundError:
            return temps
