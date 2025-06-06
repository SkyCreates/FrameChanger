import logging
import os

LOG_FILE = os.path.join(os.path.expanduser("~"), "framechanger.log")


def configure_logging():
    """Configure application-wide logging."""
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(LOG_FILE, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )

