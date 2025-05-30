"""
memlayout - Memory Layout Library

A lightweight, dependency-free Python library for managing memory layouts 
through interval-based allocation.
"""

from .interval_lib.interval import Interval
from .interval_lib.interval_lib import IntervalLib
from .utils.logger import setup_logging, get_logger, LogLevel, get_default_logger

__version__ = "0.1.0"
__all__ = ["Interval", "IntervalLib", "setup_logging", "get_logger", "LogLevel", "get_default_logger"]

# Optional: Setup a default logger when package is imported
# Uncomment the next line if you want automatic logging setup
# _default_logger = setup_logging(level=LogLevel.INFO)