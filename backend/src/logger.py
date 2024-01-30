import logging

from logging.config import dictConfig

logger = logging.getLogger(__name__)


def configure_logger() -> None:
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "correlation_id": {
                "()": "asgi_correlation_id.CorrelationIdFilter",
                "uuid_length": 32,
                "default_value": "-",
            },
        },
        "formatters": {
            "console": {
                "class": "logging.Formatter",
                "datefmt": "%H:%M:%S",
                "format": (
                    "%(levelname)s:\t\b"
                    "%(asctime)s %(name)s:%(lineno)d "
                    "[%(correlation_id)s] %(message)s"
                ),
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "filters": ["correlation_id"],
                "formatter": "console",
            },
        },
        "loggers": {
            "src": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "httpx": {
                "handlers": ["console"],
                "level": "INFO",
            },
            "asgi_correlation_id": {
                "handlers": ["console"],
                "level": "WARNING",
            },
        },
    })
    logger.info("Configured Logger")
