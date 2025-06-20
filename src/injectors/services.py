from config import config

from services import FilesService
from .connections import pg


def files() -> FilesService:
    return FilesService(
        pg_connection=pg.acquire_session(),
        upload_dir=config.upload_dir,
    )
