import flask

from injectors import files

file_router = flask.Blueprint(
    'files', __name__, url_prefix='/api/files'
)


@file_router.get('/file/')
def get_files():
    """."""
    fs = files()
    res = fs.list_files(
        page=flask.request.args.get('page'),
        page_size=flask.request.args.get('page_size'),
        prefix=flask.request.args.get('prefix'),
    )
    return flask.jsonify(res)


@file_router.get('/file/<int:file_id>/')
def get_file(file_id):
    """."""
    fs = files()
    res = fs.get_file(file_id)
    return flask.jsonify(res)


@file_router.delete('/file/<int:file_id>/')
def delete_file(file_id):
    """."""
    fs = files()
    deleted = fs.delete_file(file_id)
    return flask.jsonify({'deleted': deleted})


@file_router.post('/file/')
def create_file():
    """."""
    fs = files()
    res = fs.upload_file(
        flask.request.files.get('upload'),
        flask.request.form.get('path'),
        flask.request.form.get('comment'),
    )
    return flask.jsonify(res)


@file_router.get('/file/<int:file_id>/download/')
def download_file(file_id):
    """."""
    fs = files()
    path, filename = fs.download_file(file_id)
    return flask.send_file(
        path_or_file=path,
        download_name=filename,
        mimetype="application/octet-stream",
    )


@file_router.patch('/file/<int:file_id>/')
def update_file(file_id):
    """."""
    fs = files()
    res = fs.update_file(file_id, flask.request.json)
    return flask.jsonify(res)
