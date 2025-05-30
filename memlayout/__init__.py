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