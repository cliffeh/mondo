import os
import random

from flask import Blueprint
from mondo.util import payload

bp = Blueprint("sensors", __name__, url_prefix="/sensors")


@bp.route("/rand", methods=("GET",))
def get_rand():
    """Get random number (for testing)"""
    return payload({"rand": random.randint(20000, 90000)})


@bp.route("/temp", methods=("GET",))
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
    return payload(temps)


@bp.route("/load", methods=("GET",))
def get_load():
    """Get system load average"""
    la = os.getloadavg()
    return payload({"1m": la[0], "5m": la[1], "15m": la[2]})
