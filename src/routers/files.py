import flask

from injectors import files

file_router = flask.Blueprint(
    'tasks', __name__, url_prefix='/api/'
)

@file_router.get('/files/')
def get_files():
    """."""
    # TODO: не забыть URL параметры
    fs = files()
    res = fs.list_files()
    return flask.jsonify(res)

@file_router.get('/file/<int:file_id>')
def get_file(file_id):
    """."""
    fs = files()
    res = fs.get_file(file_id)
    return flask.jsonify(res)
