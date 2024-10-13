import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
import json

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        # Create a dictionary with the log record attributes
        log_record = {
            'timestamp': self.formatTime(record, self.datefmt),
            'name': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
        }
        
        # Add extra attributes if any
        if hasattr(record, 'extra'):
            log_record.update(record.extra)
        
        return json.dumps(log_record)

def setup_logger(name: str, log_file: str = None, level: int = logging.INFO, max_bytes: int = 10485760, backup_count: int = 5) -> logging.Logger:
    """Set up a logger with console and file handlers, including log rotation and structured logging."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Structured formatter
    formatter = StructuredFormatter()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation (optional)
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Create a default logger
default_logger = setup_logger('aigent', 'logs/aigent.log')

def get_logger(name: str = None) -> logging.Logger:
    """Get a logger. If no name is provided, return the default logger."""
    if name:
        return logging.getLogger(name)
    return default_logger

# Convenience functions for structured logging
def log_structured(logger, level, message, **kwargs):
    """Log a structured message with additional key-value pairs."""
    logger.log(level, message, extra={'extra': kwargs})

def debug(logger, message, **kwargs):
    log_structured(logger, logging.DEBUG, message, **kwargs)

def info(logger, message, **kwargs):
    log_structured(logger, logging.INFO, message, **kwargs)

def warning(logger, message, **kwargs):
    log_structured(logger, logging.WARNING, message, **kwargs)

def error(logger, message, **kwargs):
    log_structured(logger, logging.ERROR, message, **kwargs)

def critical(logger, message, **kwargs):
    log_structured(logger, logging.CRITICAL, message, **kwargs)
