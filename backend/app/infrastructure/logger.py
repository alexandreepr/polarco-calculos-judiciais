import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

for name in ("sqlalchemy.engine", "sqlalchemy.engine.Engine", "sqlalchemy.pool", "sqlalchemy.orm"):
    logger.setLevel(logging.WARNING)

stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)

logger.addHandler(stream_handler)
