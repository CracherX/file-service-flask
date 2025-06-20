from config import config
from models import *  # noqa

from .pg import PgConnectionInj

pg = PgConnectionInj(
    conf=config.pg,
)
