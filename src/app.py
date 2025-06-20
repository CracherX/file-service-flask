import os

import flask

from base_module import setup_logging, FormatDumps, ModuleException
from config import config
from injectors import pg
from models import Files  # noqa
from routers import file_router


def setup_app():
    current = flask.Flask(__name__)
    current.json_encoder = FormatDumps
    setup_logging(config.logging, FormatDumps)
    pg.setup(current)
    return current


app = setup_app()
app.register_blueprint(file_router)


@app.errorhandler(ModuleException)
def handle_app_exception(e: ModuleException):
    """."""
    if e.code == 500:
        import traceback
        traceback.print_exc()
    return flask.jsonify(e.json()), e.code


if __name__ == '__main__':
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=os.getenv('PORT', 80),
    )
