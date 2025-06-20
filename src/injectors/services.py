from config import config
from .connections import pg
from services import FilesService


def files() -> FilesService:
    return FilesService(
        pg_connection=pg.acquire_session(),
        upload_dir=config.upload_dir,
    )
