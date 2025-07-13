import allure
import logging
import sys
from datetime import datetime
import threading
from functools import wraps
import pytest

# Store original logging functions
_original_critical = logging.critical
_original_error = logging.error
_original_warning = logging.warning
_original_info = logging.info
_original_debug = logging.debug
_original_notset = logging.log

# Configuration defaults
_DEFAULT_CONFIG = {
    'buffer_size': 1000,
    'include_timestamp': True,
    'log_format': "[{timestamp}] {level}: {message}",
    'auto_flush': True,
    'min_log_level': 'DEBUG'
}

# Global configuration
_config = _DEFAULT_CONFIG.copy()

# Thread-local storage for log buffers
_log_buffer = threading.local()

def configure(**kwargs):
    """Configure the logging behavior
    
    Args:
        buffer_size (int): Maximum number of logs before auto-flush (default: 1000)
        include_timestamp (bool): Include timestamps in logs (default: True)
        log_format (str): Custom log format string (default: "[{timestamp}] {level}: {message}")
        auto_flush (bool): Enable auto-flush on buffer overflow (default: True)
        min_log_level (str): Minimum log level to capture (default: 'DEBUG')
    """
    global _config
    _config.update(kwargs)
    print(f"✅ pytest-allure-step configured: {kwargs}")

def get_config():
    """Get current configuration"""
    return _config.copy()

def reset_config():
    """Reset configuration to defaults"""
    global _config
    _config = _DEFAULT_CONFIG.copy()
    print("✅ pytest-allure-step configuration reset to defaults")

def set_buffer_size(size):
    """Set the buffer size for auto-flush"""
    configure(buffer_size=size)

def set_log_level(level):
    """Set minimum log level to capture (DEBUG, INFO, WARNING, ERROR, CRITICAL)"""
    configure(min_log_level=level.upper())

def enable_auto_flush():
    """Enable auto-flush on buffer overflow"""
    configure(auto_flush=True)

def disable_auto_flush():
    """Disable auto-flush on buffer overflow"""
    configure(auto_flush=False)

def _start_log_buffer():
    _log_buffer.logs = []

def _clear_log_buffer():
    """Clear the current log buffer"""
    if hasattr(_log_buffer, 'logs'):
        _log_buffer.logs = []

def clear_logs():
    """Public function to clear the current log buffer"""
    _clear_log_buffer()

def _buffer_log(level, message):
    if not hasattr(_log_buffer, 'logs'):
        _log_buffer.logs = []
    
    # Check minimum log level
    log_levels = {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}
    current_level = log_levels.get(level, 0)
    min_level = log_levels.get(_config['min_log_level'], 0)
    
    if current_level < min_level:
        return  # Skip logging if below minimum level
    
    # Auto-flush if buffer gets too large (prevent memory leaks)
    if _config['auto_flush'] and len(_log_buffer.logs) > _config['buffer_size']:
        _flush_log_buffer("Step Log")
    
    # Format the log message
    if _config['include_timestamp']:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    else:
        timestamp = ""
    
    # Use custom format or default
    if _config['log_format']:
        formatted_message = _config['log_format'].format(
            timestamp=timestamp,
            level=level,
            message=message
        )
    else:
        formatted_message = f"[{timestamp}] {level}: {message}"
    
    _log_buffer.logs.append(formatted_message)

def _flush_log_buffer(step_name="Step Log"):
    if hasattr(_log_buffer, 'logs') and _log_buffer.logs:
        log_text = "\n".join(_log_buffer.logs)
        allure.attach(log_text, name=step_name, attachment_type=allure.attachment_type.TEXT)
        _log_buffer.logs = []

# Override logging functions
def critical(message, *args, **kwargs):
    _original_critical(message, *args, **kwargs)
    _buffer_log("CRITICAL", message)

def error(message, *args, **kwargs):
    _original_error(message, *args, **kwargs)
    _buffer_log("ERROR", message)

def warning(message, *args, **kwargs):
    _original_warning(message, *args, **kwargs)
    _buffer_log("WARNING", message)

def info(message, *args, **kwargs):
    _original_info(message, *args, **kwargs)
    _buffer_log("INFO", message)

def debug(message, *args, **kwargs):
    _original_debug(message, *args, **kwargs)
    _buffer_log("DEBUG", message)

def log(level, message, *args, **kwargs):
    _original_notset(level, message, *args, **kwargs)
    _buffer_log(f"LOG({level})", message)

# Replace the logging functions globally
logging.critical = critical
logging.error = error
logging.warning = warning
logging.info = info
logging.debug = debug
logging.log = log

# Also replace the functions in the logging module
sys.modules['logging'].critical = critical
sys.modules['logging'].error = error
sys.modules['logging'].warning = warning
sys.modules['logging'].info = info
sys.modules['logging'].debug = debug
sys.modules['logging'].log = log


def allure_step(step_name):
    def decorator(func):
        @allure.step(step_name)
        @wraps(func)
        def wrapper(*args, **kwargs):
            _start_log_buffer()
            try:
                return func(*args, **kwargs)
            finally:
                _flush_log_buffer()
        return wrapper
    return decorator

@pytest.fixture(autouse=True)
def clear_log_buffer_before_test():
    """Automatically clear log buffer before each test to prevent log mixing"""
    _clear_log_buffer()
    yield