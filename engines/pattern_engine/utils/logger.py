"""
Logger cho Pattern Engine.
"""

import logging


class PatternLogger:

    LOGGER_NAME = "PatternEngine"

    @classmethod
    def get_logger(cls):

        logger = logging.getLogger(cls.LOGGER_NAME)

        if not logger.handlers:

            handler = logging.StreamHandler()

            formatter = logging.Formatter(

                "[%(levelname)s] %(message)s"

            )

            handler.setFormatter(formatter)

            logger.addHandler(handler)

            logger.setLevel(logging.INFO)

        return logger
