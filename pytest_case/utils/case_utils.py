from typing import Any, Callable, Dict, Tuple

from pytest_case.consts import MARKS_PARAM_NAME, PYTEST_MARKER
from pytest_case.utils.func_utils import get_func_param_names


def is_case(func: Callable[..., Any]) -> bool:
    """
    Determines if a function is marked as a 'case' using pytest.

    :param func: A function to check for the 'case' mark.
    :return: True if the function is marked with 'case', False otherwise.
    """
    func_marks = getattr(func, PYTEST_MARKER, None)
    return (
        func_marks is not None and
        next(filter(lambda mark: mark.name == "case", func_marks), None)
    )


def validate_case_inputs(
    wrapped_func: Callable[..., Any], case_args: Tuple[Any], case_kwargs: Dict[str, Any]
) -> None:
    """
    Validate the input function for compatibility with case arguments.
    """
    if not callable(wrapped_func):
        raise TypeError(f"'{wrapped_func}' is not callable")

    func_params = get_func_param_names(wrapped_func)

    if not func_params:
        raise TypeError("Test function does not take any parameters")

    total_params = len(case_args) + len(case_kwargs)
    if total_params > len(func_params):
        raise TypeError(
            f"Test '{wrapped_func.__name__}' expected {len(func_params)} \
            but got {total_params} parameters"
        )

    if MARKS_PARAM_NAME in func_params:
        raise TypeError("Function parameters cannot contain reserved keyword 'marks'")
