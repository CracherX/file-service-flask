import dataclasses as dc
import os

from src.base_module import (
    Model,
    LoggerConfig,
    FilePgConfig,
)


@dc.dataclass
class ServiceConfig(Model):
    """."""

    app_host: str = os.getenv('APP_HOST', '0.0.0.0')
    app_port: int = os.getenv('APP_PORT', 80)
    pg: FilePgConfig = dc.field(default_factory=FilePgConfig)
    logging: LoggerConfig = dc.field(default_factory=LoggerConfig)
    upload_dir: str = dc.field(default=os.getenv('UPLOAD_DIR', '/uploads'))

