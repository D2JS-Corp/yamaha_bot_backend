import sys
from pathlib import Path
from datetime import datetime

# Directorio de logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configuración de logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]"
        },
        "simple": {
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        },
        "json": {
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(filename)s %(lineno)d",
            "class": "yamaha_bot_backend.infrastructure.logging.JsonFormatter"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": sys.stdout
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": LOG_DIR / "backend.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8"
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "detailed",
            "filename": LOG_DIR / "errors.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf8"
        },
        "mqtt_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": LOG_DIR / "mqtt.log",
            "maxBytes": 10485760,
            "backupCount": 3,
            "encoding": "utf8"
        }
    },
    "loggers": {
        "yamaha_bot_backend": {
            "level": "DEBUG",
            "handlers": ["console", "file", "error_file"],
            "propagate": False
        },
        "yamaha_bot_backend.mqtt": {
            "level": "INFO",
            "handlers": ["console", "mqtt_file"],
            "propagate": False
        },
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        },
        "fastapi": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}