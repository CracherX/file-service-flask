"""."""
import dataclasses as dc
import os

import yaml

from src.base_module import (
    Model,
    LoggerConfig,
    FilePgConfig,
)


@dc.dataclass
class ServiceConfig(Model):
    """."""

    pg: FilePgConfig = dc.field(default=FilePgConfig())
    logging: LoggerConfig = dc.field(default=None)


config: ServiceConfig = ServiceConfig.load(
    yaml.safe_load(open(os.getenv('YAML_PATH', '/config.yaml'))) or {}
)
