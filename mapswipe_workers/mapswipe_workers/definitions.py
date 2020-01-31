import json
import logging
import logging.config
import os

import sentry_sdk


class CustomError(Exception):
    pass


def load_config(CONFIG_PATH) -> dict:
    """Read the configuration file."""
    with open(CONFIG_PATH) as f:
        return json.load(f)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_DIR = os.path.abspath("/usr/share/config/mapswipe_workers/")

CONFIG_PATH = os.path.join(CONFIG_DIR, "configuration.json")

CONFIG = load_config(CONFIG_PATH)

SERVICE_ACCOUNT_KEY_PATH = os.path.join(CONFIG_DIR, "serviceAccountKey.json")

LOGGING_CONFIG_PATH = os.path.join(CONFIG_DIR, "logging.cfg")

DATA_PATH = os.path.abspath("/var/lib/mapswipe_workers/")

logging.config.fileConfig(fname=LOGGING_CONFIG_PATH, disable_existing_loggers=True)
logger = logging.getLogger("Mapswipe Workers")

try:
    sentry_sdk.init(CONFIG["sentry"]["dsn"])
except KeyError:
    logger.info(
        "No configuration for Sentry was found. Continue without Sentry integration."
    )
sentry = sentry_sdk
