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
            page=int(flask.request.args.get('page')),
            page_size=int(flask.request.args.get('page_size')),
            path_contains=flask.request.args.get('path_contains'),
    )
    return flask.jsonify(res)

@file_router.get('/file/<int:file_id>')
def get_file(file_id):
    """."""
    fs = files()
    res = fs.get_file(file_id)
    return flask.jsonify(res)

@file_router.delete('/file/<int:file_id>')
def delete_file(file_id):
    """."""
    fs = files()
    deleted = fs.delete_file(file_id)
    return flask.jsonify({'deleted': deleted})

@file_router.post('/file')
def create_file():
    """."""
    fs = files()
    res = fs.upload_file(
        flask.request.files.get('upload'),
        flask.request.form.get('path'),
        flask.request.form.get('comment'),
                         )
    return flask.jsonify(res)

@file_router.get('/file/<int:file_id>/download')
def download_file(file_id):
    """."""
    fs = files()
    res = fs.download_file(file_id)
    return flask.send_file(
        path_or_file=res.get('path'),
        download_name=res.get('name'),
        mimetype="application/octet-stream",
    )
