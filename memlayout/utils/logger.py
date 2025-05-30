"""
Simple logging utility for memlayout library

Basic logger to replace print statements with configurable output levels.
"""

import logging
import sys
from enum import Enum


class LogLevel(Enum):
    """Simple log level enumeration"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR


class SimpleLogger:
    """
    Simple logger that can replace print statements
    """
    
    def __init__(self, name: str = "memlayout"):
        self.logger = logging.getLogger(name)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message (default level)"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)


def setup_logging(level: LogLevel = LogLevel.INFO, show_timestamp: bool = False) -> SimpleLogger:
    """
    Setup basic logging configuration
    
    Args:
        level: Logging level to use
        show_timestamp: Whether to show timestamps in output
        
    Returns:
        SimpleLogger instance
    """
    # Clear any existing handlers
    root_logger = logging.getLogger("memlayout")
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    root_logger.setLevel(level.value)
    
    # Simple console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level.value)
    
    # Simple format - just the message, or with timestamp
    if show_timestamp:
        formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
    else:
        formatter = logging.Formatter('%(message)s')
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Prevent propagation to avoid duplicate messages
    root_logger.propagate = False
    
    return SimpleLogger("memlayout")


def get_logger(name: str = "memlayout") -> SimpleLogger:
    """
    Get a simple logger instance
    
    Args:
        name: Logger name
        
    Returns:
        SimpleLogger instance
    """
    return SimpleLogger(name)


# Default logger instance for easy use
_default_logger: SimpleLogger = None


def get_default_logger() -> SimpleLogger:
    """Get the default logger instance, creating it if necessary"""
    global _default_logger
    if _default_logger is None:
        _default_logger = setup_logging()
    return _default_logger 