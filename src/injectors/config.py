import os

import yaml

from src.config import ServiceConfig

config: ServiceConfig = ServiceConfig.load(
    yaml.safe_load(open(os.getenv('YAML_PATH', '/config.yaml'))) or {}
)