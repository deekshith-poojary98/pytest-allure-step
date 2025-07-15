# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Future enhancements and improvements

## [0.1.0] - 2025-07-13
### Added
- Initial PyPI release
- Log buffering and auto-flush functionality
- Allure step integration with decorator support
- Thread-safe implementation for concurrent test execution
- Comprehensive configuration system with multiple options
- Manual and decorator-based logging approaches
- Automatic log cleaning fixture for test isolation
- Enhanced documentation and project badges
- Support for custom log formats and timestamps
- Buffer size management and auto-flush controls
- Minimum log level filtering capabilities

### Features
- `@allure_step` decorator for automatic log capture
- `configure()` function for runtime configuration
- `clear_logs()` function for manual buffer management
- Thread-local storage for isolated log buffers
- Integration with pytest fixtures for automatic cleanup
