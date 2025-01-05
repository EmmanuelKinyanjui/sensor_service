import os

from dotenv import load_dotenv

# load environment variable from .env file
load_dotenv(os.getenv("ENV_FILE", ".env"))

# environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

# database
DATABASE_URL = os.getenv("DATABASE_URL")

# redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {"": {"handlers": ["default"], "level": "INFO", "propagate": True}},
}
