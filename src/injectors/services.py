from config import config
from ..services.files import FilesService
from pg import pg


def files() -> FilesService:
    return FilesService(
        pg_connection=pg,
        upload_dir=config.upload_dir,
    )