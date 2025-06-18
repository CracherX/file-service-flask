from config import config
from .pg import pg
from services import FilesService


def files() -> FilesService:
    return FilesService(
        pg_connection=pg,
        upload_dir=config.upload_dir,
    )