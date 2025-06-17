import os

import flask

import routers
from config import config
from base_module import setup_logging, FormatDumps, ModuleException
from injectors.connections import pg


def setup_app():
    current = flask.Flask(__name__)
    current.json_encoder = FormatDumps
    pg.setup(current)
    setup_logging(config.logging, FormatDumps)
    oms_setup_routers(
        app=current,
        config=config.config_data,
        static_dir=config.static_dir,
        mv=middleware.oms_middleware
    )

    return current


app = setup_app()
app.register_blueprint(routers.tasks_routers)


@app.errorhandler(ModuleException)
def handle_app_exception(e: ModuleException):
    """."""
    if e.code == 500:
        import traceback
        traceback.print_exc()
    return flask.jsonify(e.json()), e.code


if __name__ == '__main__':
    app.run(
        host=os.getenv('APP_HOST', '0.0.0.0'),
        port=os.getenv('APP_PORT', 80)
    )