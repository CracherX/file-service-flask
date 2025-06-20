import os
import dataclasses as dc
from datetime import datetime, UTC
from pathlib import Path
from shutil import move
from typing import Optional, List
from uuid import uuid4

from sqlalchemy.orm import Session as PGSession

from base_module import ClassesLoggerAdapter, Model
from models import Files


@dc.dataclass
class CreationModel(Model):
    """."""
    name: str = dc.field(metadata={'required': True})
    extension: Optional[str] = dc.field(metadata={'required': False})
    size: int = dc.field(metadata={'required': True})
    path: str = dc.field(metadata={'required': True})
    comment: Optional[str] = dc.field(metadata={'required': False})


@dc.dataclass
class UpdateModel(Model):
    """."""
    file_id: int = dc.field(metadata={'required': True})
    name: Optional[str] = dc.field(metadata={'required': False})
    path: Optional[str] = dc.field(metadata={'required': False})
    comment: Optional[str] = dc.field(metadata={'required': False})


class DownloadModel(Model):
    """."""
    path: str = dc.field(metadata={'required': True})
    filename: str = dc.field(metadata={'required': True})


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
            page: int = 1,
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

    def get_file(self, file_id: int) -> Files | None:
        self._logger.info(
            'Запрошен файл',
            extra={
                'file_id': file_id
            }
        )
        return self._pg.query(Files).filter(Files.id == file_id).first()

    def delete_file(self, file_id: int) -> bool:
        self._logger.info(
            'Удаление файла',
            extra={
                'file_id': file_id
            }
        )
        file = self.get_file(file_id)
        if not file:
            self._logger.info(
                'Файл не найден',
                extra={
                    'file_id': file_id
                }
            )
            return False

        full_path = Path(
            __file__).resolve().parent.parent / self._upload / file.path / f"{file.name}.{file.extension}"

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

        file_phys = self._pg.query(Files).filter(Files.id == file_id).first()
        if file_phys:
            self._pg.delete(file)
            self._pg.commit()

        self._logger.info(
            'Файл удалён',
            extra={
                'file_id': file_id,
                'file_path': full_path
            }
        )
        return True

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

        path = Path(__file__).resolve().parent.parent / self._upload / data.path
        path.mkdir(parents=True, exist_ok=True)

        file_path = path / f"{data.name}.{data.extension}"

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
        self._pg.add(file)
        self._pg.commit()
        self._pg.refresh(file)
        return file

    def download_file(self, file_id: int) -> dict[str, str] | None:
        self._logger.info(
            'Запрос на скачивание файла',
            extra={'file_id': file_id},
        )
        file = self.get_file(file_id)
        if not file:
            self._logger.info(
                'Файл не найден',
                extra={'file_id': file_id},
            )
            return None

        base_dir = Path(__file__).resolve().parent.parent

        full_path = base_dir / self._upload / file.path
        if file.extension != '':
            full_path = full_path / f'{file.name}.{file.extension}'
        else:
            full_path = full_path / file.name

        if not full_path.exists():
            self._logger.warning(
                'Файл не найден на диске',
                extra={'full_path': full_path},
            )
            return None

        self._logger.info(
            'Файл готов к скачиванию',
            extra={'file_id': file_id},
        )
        return {
            'path': str(full_path),
            'name': f'{file.name}.{file.extension}',
        }

    def update_file(self, data) -> Files | None:
        data = UpdateModel.load(data)
        self._logger.info(
            'Начало обновления файла',
            extra={'file_id': data.file_id},
        )
        file = self.get_file(data.file_id)
        if not file:
            self._logger.info(
                'Указанный файл не найден',
                extra={'file_id': data.file_id},
            )
            return None

        old_path = Path(__file__).resolve().parent.parent / self._upload / file.path
        if file.extension != '':
            old_path = old_path / f'{file.name}.{file.extension}'
        else:
            old_path = old_path / file.name

        new_name = data.name or file.name
        new_path = data.path or file.path
        new_file_path = Path(__file__).resolve().parent.parent / self._upload / new_path
        new_file_path.mkdir(parents=True, exist_ok=True)

        if file.extension != '':
            new_file_path = new_file_path / f'{new_name}.{file.extension}'
        else:
            new_file_path = new_file_path / f'{new_name}'

        if data.name or data.path:
            if old_path.exists():
                move(str(old_path), str(new_file_path))
                self._logger.info(
                    'Файл перемещен',
                    extra={
                        'file_id': data.file_id,
                        'old_path': old_path,
                        'new_path': new_file_path,
                    },
                )
            else:
                self._logger.warning(
                    'Старый файл не найден на диске',
                    extra={'old_file_path': old_path}
                )

        file.name = data.name
        file.path = data.path
        file.comment = data.comment
        file.updated_at = datetime.now(UTC)

        self._pg.commit()
        self._pg.refresh(file)

        self._logger.info(
            'Файл обновлён в базе данных',
            extra={'file_id': data.file_id},
                          )
        return file
