import logging
from contextlib import contextmanager

import coloredlogs


def pretty_logging(level: str = "INFO"):
    coloredlogs.install(
        level=level,
        # NOTE: force color when this is executed via subprocess
        isatty=True,
    )


@contextmanager
def quiet_httpx_logging():
    try:
        existing_level = logging.getLogger("httpx").level
        logging.getLogger("httpx").setLevel(logging.WARNING)
        yield
    finally:
        logging.getLogger("httpx").setLevel(existing_level)
