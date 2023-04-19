import logging
from typing import Type

def create_logger(name: str, level: Type[int] | Type[str]=logging.INFO):
    _logger = logging.getLogger(name)

    # set stream handler
    _formater = logging.Formatter(
        fmt="%(asctime)s [%(process)s] [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    _stream = logging.StreamHandler()
    _stream.setFormatter(_formater)

    # set logger
    _logger.addHandler(_stream)
    _logger.setLevel(level)
    return _logger
