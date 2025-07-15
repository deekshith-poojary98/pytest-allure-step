# Pytest Allure Step Logger

[![PyPI version](https://badge.fury.io/py/pytest-allure-step.svg)](https://badge.fury.io/py/pytest-allure-step)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/pytest-allure-step.svg)](https://pypi.org/project/pytest-allure-step/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/pytest-allure-step?period=total&units=international_system&left_color=gray&right_color=orange&left_text=downloads)](https://pepy.tech/project/pytest-allure-step)


A robust, plug-and-play logging integration for pytest and Allure. Automatically captures, buffers, and attaches logs to Allure test steps—no code changes required. Highly configurable, thread-safe, and designed for clean, isolated test reporting.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Logging Inside and Outside Decorators](#logging-inside-and-outside-decorators)
  - [Manual Log Clearing](#manual-log-clearing)
  - [Configuration](#configuration)
  - [Best Practices](#best-practices)
  - [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)
- [Behavioral Details](#behavioral-details)
- [Requirements](#requirements)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Changelog](#changelog)

---

## Features
- 📝 **Automatic Log Capture**: All logging calls are captured and buffered, even outside decorators.
- 🔄 **Allure Step Integration**: Logs are attached to Allure test steps for traceability.
- 🔒 **Thread-Safe**: Each test/thread gets its own buffer.
- 🧹 **Automatic Cleanup**: Log buffer is cleared before each test to prevent log mixing.
- ⚙️ **Highly Configurable**: Buffer size, log format, min log level, auto-flush, and more.
- ✨ **Zero Code Changes**: Works with standard `logging` calls out of the box.
- 🎯 **Manual & Decorator Support**: Use decorators for step-level logs, or log directly.

---

## Installation

```bash
pip install pytest-allure-step
```

> **Note:** Allure reports require the [Allure CLI](https://docs.qameta.io/allure/#_installing_a_commandline) to be installed and available in your PATH.

---

## Quick Start

### Basic Usage with Decorator
```python
import logging
from pytest_allure_step import allure_step

@allure_step("My Test Step")
def my_step():
    logging.info("This log will be captured and attached to the Allure step")
    logging.error("Error messages are also captured")
    return True

def test_example():
    result = my_step()
    assert result
```

### Direct Logging (No Decorator)
```python
from pytest_allure_step import info, warning, error, debug, critical, log

def test_direct_logging():
    info("This is an info message")
    warning("This is a warning")
    error("This is an error")
    debug("Debug message")
    critical("Critical error!")
    log(25, "Custom log level message")
    assert True
```

---

## Usage

### Logging Inside and Outside Decorators
- **Inside `@allure_step`**: Logs are attached to the step and flushed at the end.
- **Outside decorator**: Logs are buffered and auto-flushed on buffer overflow. Remaining logs are not attached unless you flush or use a decorator.

#### Example: Buffer Overflow (Auto-Flush)
```python
from pytest_allure_step import configure, info

def test_buffer():
    configure(buffer_size=3)
    for i in range(5):
        info(f"Message {i}")  # After 3, auto-flush triggers and attaches logs
```

### Manual Log Clearing
```python
from pytest_allure_step import clear_logs, info

def test_manual_clear():
    info("Before clear")
    clear_logs()  # Flushes and clears buffer
    info("After clear")
```

### Configuration
```python
from pytest_allure_step import configure, set_log_level

configure(
    buffer_size=500,
    min_log_level="WARNING",
    log_format="[{timestamp}] {level} | {message}",
    auto_flush=True
)
set_log_level("ERROR")
```

#### Configuration Options
| Option              | Default                                 | Description                           |
|---------------------|-----------------------------------------|---------------------------------------|
| `buffer_size`       | 1000                                    | Max logs before auto-flush            |
| `include_timestamp` | True                                    | Include timestamps in log messages    |
| `log_format`        | `"[{timestamp}] {level}: {message}"`    | Custom log format string              |
| `auto_flush`        | True                                    | Auto-flush on buffer overflow         |
| `min_log_level`     | "DEBUG"                                 | Minimum log level to capture          |

### Best Practices
- Use `@allure_step` for step-level log grouping.
- For logs outside decorators, call `clear_logs()` at the end if you want all logs attached.
- Adjust `buffer_size` for your test suite’s needs.
- Use `set_log_level` to reduce noise in large test runs.

### Troubleshooting
- **Logs missing in Allure?**
  - Ensure you use the decorator or call `clear_logs()` at the end of your test.
  - Check your buffer size and auto-flush settings.
- **Allure CLI not found?**
  - Install Allure CLI and add it to your PATH.
- **Log mixing between tests?**
  - Automatic cleanup is enabled by default; if you see mixing, check for custom threading or multiprocessing.

---

## API Reference

### Logging Functions
- `critical(message, *args, **kwargs)`
- `error(message, *args, **kwargs)`
- `warning(message, *args, **kwargs)`
- `info(message, *args, **kwargs)`
- `debug(message, *args, **kwargs)`
- `log(level, message, *args, **kwargs)`

### Configuration Functions
- `configure(**kwargs)`
- `get_config()`
- `reset_config()`
- `set_buffer_size(size)`
- `set_log_level(level)`
- `enable_auto_flush()`
- `disable_auto_flush()`
- `clear_logs()`

### Decorators
- `@allure_step(step_name)`

### Fixtures
- **Automatic log cleaning**: A pytest fixture is included and enabled by default, clearing the log buffer before each test.

---

## Behavioral Details
- **Buffering**: Logs are buffered in thread-local storage.
- **Auto-Flush**: When buffer exceeds `buffer_size`, logs are attached to Allure and buffer is cleared.
- **Decorator**: `@allure_step` flushes logs at the end of the step.
- **Manual Clear**: `clear_logs()` flushes and clears the buffer.
- **Automatic Cleanup**: Buffer is cleared before each test (via fixture).
- **Thread Safety**: Each thread/test gets its own buffer.

---

## Requirements
- Python 3.7+
- pytest >= 6.0.0
- allure-pytest >= 2.9.0

---

## Development

### Install for Development
```bash
git clone https://github.com/deekshith-poojary98/pytest-allure-step.git
cd pytest-allure-step
pip install -e .[dev]
```

### Run Tests
```bash
pytest
```

### Code Quality
```bash
black pytest_allure_step/
flake8 pytest_allure_step/
mypy pytest_allure_step/
```

---

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes (add tests!)
4. Run the test suite
5. Submit a pull request

Please see [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

---

## License
MIT License. See [LICENSE](LICENSE).

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history. 
