from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.orm.decl_api import as_declarative, declared_attr


@as_declarative()
class Base:
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Files(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    extension = Column(String(10), nullable=True)
    size = Column(Integer, nullable=False)
    path = Column(String(1024), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    comment = Column(Text, nullable=True)

    __table_args__ = (
        Index('ix_files_path', 'path'),
    )

    def __repr__(self):
        return f"<File(name={self.name!r}, extension={self.extension!r}, size={self.size}, path={self.path!r})>"