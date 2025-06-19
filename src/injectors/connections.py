from .pg import PgConnectionInj
from config import config
from models import *  # noqa

pg = PgConnectionInj(
    conf=config.pg,
)
