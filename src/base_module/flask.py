import datetime
from enum import Enum
from uuid import UUID

import flask

from . import Model


class FormatDumps(flask.json.JSONEncoder):
    """."""

    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        if isinstance(o, UUID):
            return o.hex
        if isinstance(o, Model):
            return o.dump()
        if isinstance(o, Enum):
            return o.value

        try:
            from shapely.geometry.base import BaseGeometry
            from shapely.geometry import mapping
            if isinstance(o, BaseGeometry):
                return mapping(o)
        except (ImportError, ModuleNotFoundError):
            pass

        try:
            return flask.json.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)
