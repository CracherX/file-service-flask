import flask

from injectors import files

file_router = flask.Blueprint(
    'tasks', __name__, url_prefix='/api/'
)

@file_router.get('/files/')
def get_files():
    """."""
    fs = files()
    res = fs.list_files(
            page=flask.request.args.get('page'),
            page_size=flask.request.args.get('page_size'),
            path_contains=flask.request.args.get('path_contains'),
    )
    return flask.jsonify(res)

@file_router.get('/file/<int:file_id>')
def get_file(file_id):
    """."""
    fs = files()
    res = fs.get_file(file_id)
    return flask.jsonify(res)
