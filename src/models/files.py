import dataclasses as dc
import typing
from datetime import datetime

import sqlalchemy as sa
from base_module import BaseOrmMappedModel
from sqlalchemy import Index


@dc.dataclass
class Files(BaseOrmMappedModel):
    __tablename__ = 'files'
    __table_args__ = (
        Index('ix_files_path', 'path'),
        {'schema': 'public'}
    )

    id: typing.Optional[int] = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.Integer, primary_key=True, index=True)}
    )
    name: str = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.String(255), nullable=False)}
    )
    extension: typing.Optional[str] = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.String(10), nullable=True)}
    )
    size: int = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.Integer, nullable=False)}
    )
    path: str = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.String(1024), nullable=False)}
    )
    created_at: datetime = dc.field(
        default_factory=datetime.utcnow,
        metadata={'sa': sa.Column(sa.DateTime, nullable=False)}
    )
    updated_at: typing.Optional[datetime] = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.DateTime, nullable=True)}
    )
    comment: typing.Optional[str] = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.Text, nullable=True)}
    )

    def __repr__(self):
        return f"<File(name={self.name!r}, path={self.path!r})>"


BaseOrmMappedModel.REGISTRY.mapped(Files)
