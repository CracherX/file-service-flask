from typing import Optional, List

import sqlalchemy as sa
from sqlalchemy.orm import Session as PGSession

from src.base_module import ClassesLoggerAdapter
from src.models import Files


class FilesService:
    def __init__(
            self,
            pg_connection: PGSession,
            upload_dir: str,
    ):
        self._pg = pg_connection
        self._logger = ClassesLoggerAdapter.create(self)
        self.upload = upload_dir

        def list_files(
                self,
                page: int = 0,
                page_size: int = 100,
                path_contains: Optional[str] = None
        ) -> list[type[Files]]:
            offset = (page - 1) * page_size
            self._logger.info(
                f"Запрошен список файлов: страница {page}, размер страницы {page_size}, фильтр: {path_contains}")
            query = self._pg.query(Files)
            if path_contains:
                query = query.filter(Files.path.contains(path_contains))
            return query.offset(offset).limit(page_size).all()