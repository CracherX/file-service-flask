import dataclasses as dc
import os
from datetime import datetime, UTC
from pathlib import Path
from shutil import move
from typing import Optional, List
from uuid import uuid4

from base_module import (
    ClassesLoggerAdapter,
    Model,
    ModuleException
)
from models import Files
from sqlalchemy.orm import Session as PGSession


@dc.dataclass
class CreationModel(Model):
    """."""
    name: str = dc.field()
    extension: Optional[str] = dc.field()
    size: int = dc.field()
    path: str = dc.field()
    comment: Optional[str] = dc.field()


@dc.dataclass
class UpdateModel(Model):
    """."""
    name: Optional[str] = dc.field(default=None)
    path: Optional[str] = dc.field(default=None)
    comment: Optional[str] = dc.field(default=None)


class FilesService:
    def __init__(
            self,
            pg_connection: PGSession,
            upload_dir: str,
    ):
        self._pg = pg_connection
        self._logger = ClassesLoggerAdapter.create(self)
        self._upload = upload_dir

    def list_files(
            self,
            page: str = 1,
            page_size: str = 100,
            prefix: Optional[str] = None
    ) -> List[Files]:

        self._logger.info(
            'Запрошен список файлов',
            extra={
                'page': page,
                'page_size': page_size
            }
        )
        try:
            page = int(page)
            page_size = int(page_size)
        except:
            self._logger.info(
                'Ошибка в параметрах URL',
                extra={
                    'page': page,
                    'page_size': page_size
                }
            )
            raise ModuleException(
                'Параметры не являются числами или не указаны вовсе',
                code=400
            )

        offset = (page - 1) * page_size
        with self._pg.begin():
            query = self._pg.query(Files)
            if prefix:
                query = query.filter(Files.path.contains(prefix))
            return query.offset(offset).limit(page_size).all()

    def get_file(self, file_id: int) -> Files | None:
        self._logger.info(
            'Запрошен файл',
            extra={
                'file_id': file_id
            }
        )
        with self._pg.begin():
            file = self._pg.query(Files).filter(Files.id == file_id).first()
            if file:
                return file
        self._logger.info(
            'Файл не найден',
            extra={
                'file_id': file_id
            }
        )
        raise ModuleException(
            "Файл не найден",
            code=404,
        )

    def delete_file(self, file_id: int) -> None:
        self._logger.info(
            'Удаление файла',
            extra={
                'file_id': file_id
            }
        )
        file = self.get_file(file_id)

        full_path = Path(__file__) / self._upload / file.path / f"{file.name}.{file.extension}"

        if full_path.exists():
            os.remove(full_path)
            self._logger.info(
                'Файл удален с диска',
                extra={
                    'file_id': full_path
                }
            )
        else:
            self._logger.warning(
                'Файл не найден на диске',
                extra={
                    'file_id': file_id
                }
            )
        with self._pg.begin():
            self._pg.delete(file)

        self._logger.info(
            'Файл удалён',
            extra={
                'file_id': file_id,
                'file_path': full_path
            }
        )

    def upload_file(self, file, path, comment) -> Files:
        self._logger.info(
            'Загрузка файла',
            extra={
                'file_name': file.filename,
            }
        )

        content = file.read()

        filename = file.filename
        name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1].lstrip(".")
        size = len(content)

        data = CreationModel(
            name=name,
            extension=extension,
            size=size,
            path=path,
            comment=comment,
        )

        path = Path(self._upload).resolve() / data.path
        path.mkdir(parents=True, exist_ok=True)

        if data.extension:
            file_path = path / f'{data.name}.{data.extension}'
        else:
            file_path = path / data.name

        if file_path.exists():
            self._logger.warning(
                'Файл уже существует: создаётся уникальное имя',
                extra={
                    'file_path': file_path,
                }
            )
            unique_suffix = uuid4().hex[:8]
            new_name = f'{data.name}_{unique_suffix}'
            file_path = path / f'{new_name}.{data.extension}'
            data.name = new_name

        with open(file_path, 'wb') as f:
            f.write(content)

        self._logger.info(
            'Файл успешно сохранён на диск',
            extra={
                'file_path': file_path
            }
        )

        file = Files(
            name=data.name,
            extension=data.extension,
            size=data.size,
            path=data.path,
            comment=data.comment,
        )
        with self._pg.begin():
            self._pg.add(file)

        return file

    def download_file(self, file_id: int) -> tuple[str, str] | None:
        self._logger.info(
            'Запрос на скачивание файла',
            extra={'file_id': file_id},
        )
        file = self.get_file(file_id)

        full_path = Path(self._upload).resolve() / self._upload / file.path
        if file.extension != '':
            full_path = full_path / f'{file.name}.{file.extension}'
        else:
            full_path = full_path / file.name

        if not full_path.exists():
            self._logger.warning(
                'Файл не найден на диске',
                extra={'full_path': full_path},
            )
            raise ModuleException('Файл не найден', code=404)

        self._logger.info(
            'Файл готов к скачиванию',
            extra={'file_id': file_id},
        )
        return str(full_path), f'{file.name}.{file.extension}'

    def update_file(self, file_id, data) -> Files | None:
        data = UpdateModel.load(data)
        self._logger.info(
            'Начало обновления файла',
            extra={'file_id': file_id},
        )
        file = self.get_file(file_id)

        old_path = Path(self._upload).resolve() / file.path
        if file.extension != '':
            old_path = old_path / f'{file.name}.{file.extension}'
        else:
            old_path = old_path / file.name

        new_name = data.name or file.name
        new_path = data.path or file.path
        new_file_path = Path(self._upload).resolve() / new_path
        new_file_path.mkdir(parents=True, exist_ok=True)

        if file.extension != '':
            new_file_path = new_file_path / f'{new_name}.{file.extension}'
        else:
            new_file_path = new_file_path / new_name

        if data.name or data.path:
            if old_path.exists():
                move(str(old_path), str(new_file_path))
                self._logger.info(
                    'Файл перемещен',
                    extra={
                        'file_id': file_id,
                        'old_path': old_path,
                        'new_path': new_file_path,
                    },
                )
            else:
                self._logger.warning(
                    'Старый файл не найден на диске',
                    extra={'old_file_path': old_path}
                )
                raise ModuleException('Файл не найден', code=404)

        with self._pg.begin():
            file.update(data.__dict__)
            file.updated_at = datetime.now(UTC)

        self._logger.info(
            'Файл обновлён в базе данных',
            extra={'file_id': file_id},
        )
        return file
