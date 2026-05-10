import logging
from rag_demo.config import settings

logger = logging.getLogger(__name__)
def init_logger() -> logging.Logger:
    """Initialize the logger
    Returns:
        logging.Logger: The logger
    """
    try:
        log_level = settings.log_level.upper()
        level = logging.getLevelName(log_level)
        logger.setLevel(level)
        return logger
    except Exception as e:
        logger.error(f"Error initializing logger: {e}")
        return logger