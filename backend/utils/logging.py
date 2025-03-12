import logging
import logging.config
import os, json
from datetime import datetime

def setup_logging(
    log_dir="logs",
    log_level=logging.INFO,
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
    log_file_prefix="log"
):
    """
    Setup centralized logging configuration for the entire application.
    
    Args:
        log_dir (str): Directory to store log files
        log_level (int): Logging level (e.g., logging.DEBUG, logging.INFO)
        log_format (str): Format string for log messages
        log_file_prefix (str): Prefix for log file names
    """
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_filename = f"{log_file_prefix}_{timestamp}.log"
    log_filepath = os.path.join(log_dir, log_filename)
    
    # Define logging configuration
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': log_format
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': log_level,
                'formatter': 'standard',
                'filename': log_filepath,
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console', 'file'],
                'level': log_level,
            },
            '__main__': {
                'handlers': ['console', 'file'],
                'level': log_level,
                'propagate': False
            },
            'uvicorn': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
            'openai': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
            'httpcore': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
            'httpx': {
                'handlers': [],
                'level': 'CRITICAL',
                'propagate': False
            }
        },
        'disable_existing_loggers': False
    }
    
    # Apply configuration
    logging.config.dictConfig(config)
    
    # Return logger for convenience
    return logging.getLogger(__name__)

# Example usage
if __name__ == "__main__":
    logger = setup_logging(log_level=logging.DEBUG)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
