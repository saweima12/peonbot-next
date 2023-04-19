import logging
from peonbot.utils.log_util import create_logger


def test_logger():
    logger = create_logger("test")

    assert logger.level == logging.INFO
    assert logger.name == "test"