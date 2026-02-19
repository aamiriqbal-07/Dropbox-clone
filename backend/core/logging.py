import logging
import sys
from .config import settings
from .request_id import request_id_ctx

class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_ctx.get()
        return True

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(settings.log_file)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s'
    ))
    file_handler.addFilter(RequestIDFilter())
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(request_id)s] - %(message)s'
    ))
    console_handler.addFilter(RequestIDFilter())
    logger.addHandler(console_handler)

    return logger