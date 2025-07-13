"""
Pytest Allure Step Logger

A Python package that provides enhanced logging integration with Allure reports for pytest.
Automatically captures and attaches log messages to Allure test steps.
"""

from .allure_logger import (
    allure_step,
    critical,
    error,
    warning,
    info,
    debug,
    log,
    configure,
    get_config,
    reset_config,
    set_buffer_size,
    set_log_level,
    enable_auto_flush,
    disable_auto_flush,
    clear_logs
)

__version__ = "0.1.0"
__author__ = "Deekshith Poojary"
__email__ = "deekshithpoojary355@gmail.com"

__all__ = [
    "allure_step",
    "critical",
    "error", 
    "warning",
    "info",
    "debug",
    "log",
    "configure",
    "get_config",
    "reset_config",
    "set_buffer_size",
    "set_log_level",
    "enable_auto_flush",
    "disable_auto_flush",
    "clear_logs"
] 