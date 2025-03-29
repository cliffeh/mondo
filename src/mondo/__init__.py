from quart import Quart, render_template

from .api import bp as metrics_bp
from .tasks import update_metrics


def create_app(test_config=None):
    # create and configure the app
    app = Quart(__name__, static_url_path="/")
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # start collecting metrics
    @app.before_serving
    async def startup():
        app.add_background_task(update_metrics)

    @app.route("/index.html")
    @app.route("/", strict_slashes=False)
    async def index():
        return await render_template("index.html.j2", context=app.config)

    app.register_blueprint(metrics_bp)

    return app
