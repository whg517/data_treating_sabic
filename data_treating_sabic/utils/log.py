import os
from logging.config import dictConfig

from . import settings


def verbose_formatter(verbose: bool) -> str:
    if verbose is True:
        return 'verbose'
    else:
        return 'simple'


LOG_LEVEL = settings.LOGLEVEL

os.makedirs(os.path.dirname(settings.LOGFILE), exist_ok=True)

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(name)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    "handlers": {
        "console": {
            "formatter": verbose_formatter(settings.VERBOSE),
            'level': 'DEBUG',
            "class": "logging.StreamHandler",
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': verbose_formatter(settings.VERBOSE),
            'filename': settings.LOGFILE,
            'maxBytes': 1024 * 1024 * 1024 * 200,  # 200M
            'backupCount': '5',
            'encoding': 'utf-8'
        },
    },
    "loggers": {
        '': {'level': LOG_LEVEL, 'handlers': ['console', 'file']},
    }
}


def configure_logging():
    dictConfig(DEFAULT_LOGGING)
