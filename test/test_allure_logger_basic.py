import logging
from pytest_allure_step import allure_step, info, warning

def test_logging_without_decorator():
    info("This is an info log without decorator.")
    warning("This is a warning log without decorator.")
    logging.error("This is an error log without decorator.")
    assert True

@allure_step("Step: Decorated Logging")
def my_step():
    info("This is an info log with decorator.")
    warning("This is a warning log with decorator.")
    logging.error("This is an error log with decorator.")
    return True

def test_logging_with_decorator():
    result = my_step()
    assert result