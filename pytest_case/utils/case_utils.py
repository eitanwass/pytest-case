from typing import Any, Callable

from pytest_case.consts import PYTEST_MARKER


def is_case(func: Callable[..., Any]) -> bool:
    """
    Determines if a function is marked as a 'case' using pytest.

    :param func: A function to check for the 'case' mark.
    :return: True if the function is marked with 'case', False otherwise.
    """
    func_marks = getattr(func, PYTEST_MARKER, None)
    return func_marks is not None and next(filter(lambda mark: mark.name == "case", func_marks), None)
