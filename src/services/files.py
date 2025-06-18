from typing import Optional, List

from sqlalchemy.orm import Session as PGSession

from base_module import ClassesLoggerAdapter
from models import Files


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
    ) -> List[Files]:
        offset = (page - 1) * page_size
        self._logger.info(
            'Запрошен список файлов',
            extra={
                'offset': offset,
                'page': page,
                'page_size': page_size
            }
        )
        query = self._pg.query(Files)
        if path_contains:
            query = query.filter(Files.path.contains(path_contains))
        return query.offset(offset).limit(page_size).all()

    def get_file(self, file_id: str) -> Files:
        self._logger.info(
            'Запрошен файл',
            extra={
                'file_id': file_id
            }
        )
        return self._pg.query(Files).filter(Files.id == file_id).first()

    def add_file(self):
        raise NotImplementedError()
    # TODO: добавить реализацию
