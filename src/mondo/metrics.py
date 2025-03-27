import os
import random
from functools import wraps
from quart import Blueprint, request

bp = Blueprint("metrics", __name__, url_prefix="/metrics")


def filter(func):
    """custom decorator for filtering only keys the user wants"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if filters := request.args.get("filter"):
            return {key: result[key] for key in filters.split(",") if key in result}
        else:
            return result

    return wrapper


@bp.route("/rand", methods=("GET",))
def get_rand():
    """Get random number (for testing)"""
    return {"rand": float(random.randint(20000, 90000)) / 1000.0}


@bp.route("/temp", methods=("GET",))
@filter
def get_temp():
    """Get system temperature sensor values"""
    i = 0
    temps = {}
    while True:
        try:
            with open(f"/sys/class/thermal/thermal_zone{i}/temp") as tempfile, open(
                f"/sys/class/thermal/thermal_zone{i}/type"
            ) as typefile:
                temp = float(tempfile.read().strip()) / 1000.0  # convert to degrees C
                type = typefile.read().strip()
                # NB this could mean overwriting a previous value if there are
                # multiple sensors with the same name
                temps[type] = temp
            i += 1
        except FileNotFoundError:
            break
    return temps


@bp.route("/load", methods=("GET",))
@filter
def get_load():
    """Get system load average"""
    la = os.getloadavg()
    return {"1m": la[0], "5m": la[1], "15m": la[2]}
