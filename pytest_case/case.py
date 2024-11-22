from __future__ import annotations

from functools import reduce
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Union, overload

import pytest
from _pytest.mark import ParameterSet

from pytest_case.consts import MARKS_PARAM_NAME, PYTEST_MARKER
from pytest_case.types import UnwrappedFunc
from pytest_case.utils.case_utils import is_case, validate_case_inputs
from pytest_case.utils.func_utils import get_func_optional_params, get_func_param_names

__all__ = ["case"]


@overload
def case(cases_generator: Iterable[Any]) -> Callable[..., Any]: ...

@overload
def case(name: str, *args: Any, **kwargs: Any) -> Callable[..., Any]: ...


def wrap_func(
    argnames: Sequence[str],
    param_sets: List[ParameterSet],
    defaults: Dict[str, Any],
) -> Callable[..., Callable[..., Any]]:
    """
    Wraps a function with `pytest.mark.case` and `pytest.mark.parametrize`.
    Should be unwrapped manually if another case is applied
    """
    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        return pytest.mark.parametrize(
            argnames=argnames,
            argvalues=param_sets,
        )(pytest.mark.case(defaults=defaults)(func))
    return wrapper


def unwrap_func(func: Callable[..., Any]) -> UnwrappedFunc:
    """
    Unwraps a case function into its original function and its pytest-case components.
    """
    func_markers: Optional[List[pytest.MarkDecorator]] = getattr(func, PYTEST_MARKER, None)
    if func_markers is None:
        # Assumming func is a case
        raise AttributeError("Trying to unwrap a non-pytest function!")

    case_kwargs = {}
    extra_markers: List[pytest.MarkDecorator] = []
    for mark in func_markers:
        if mark.name in ["case", "parametrize"]:
            case_kwargs.update(mark.kwargs)
        else:
            extra_markers.append(mark)

    delattr(func, PYTEST_MARKER)

    return UnwrappedFunc(
        unwrapped_func=func,
        func_markers=extra_markers,
        **case_kwargs
    )


def _generator_case(
    gen: Iterable[Any], func: Callable[..., Any], **kwargs: Any
) -> Callable[..., Any]:
    """
    Generate cases from a generator (or any iterable)
    """
    case_name_template = kwargs.get("name", "{_index}")
    return reduce(
        lambda acc, params: case(
            case_name_template.format(*params[1], _index=params[0]),
            *params[1]
        )(acc),
        enumerate(gen),
        func
    )


def case(name_or_gen: Union[str, Iterable[Any]], *args: Any, **kwargs: Any) -> Callable[..., Any]:
    """
    Decorator to define test cases for pytest.
    """
    marks = kwargs.pop(MARKS_PARAM_NAME, None) or tuple()

    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        # Can't check for `Iterable` because `str` is also iterable
        if not isinstance(name_or_gen, str):
            return _generator_case(name_or_gen, func, **kwargs)
        name = name_or_gen

        validate_case_inputs(func, args, kwargs)

        argnames = []
        defaults: Dict[str, Any] = {}
        case_param_sets: List[ParameterSet] = []

        if is_case(func):
            # If wrapping an existing case
            unwrapped_func_attrs = unwrap_func(func)
            func = unwrapped_func_attrs.unwrapped_func
            argnames = unwrapped_func_attrs.argnames
            case_param_sets = unwrapped_func_attrs.argvalues
            defaults = unwrapped_func_attrs.defaults
        else:
            # If wrapping a new test function
            func_params = get_func_param_names(func)
            defaults = get_func_optional_params(func)
            func_required_params = func_params[: len(func_params) - len(defaults)]
            # All the rest should be fixtures or will raise an error because tey are not provided
            argnames = (*func_required_params, *defaults.keys())

            func.__defaults__ = None

        case_argvalues = []
        for arg_index, argname in enumerate(argnames):
            new_argvalue = None

            if argname in defaults:
                # Has default value - use it
                new_argvalue = defaults[argname]

            if arg_index < len(args):
                # Provided in args - use it
                new_argvalue = args[arg_index]

            if argname in kwargs:
                # Provided in kwargs - use it
                new_argvalue = kwargs[argname]

            case_argvalues.append(new_argvalue)

        case_param_sets = [pytest.param(*case_argvalues, marks=marks, id=name)] + case_param_sets

        return wrap_func(
            argnames=argnames,
            param_sets=case_param_sets,
            defaults=defaults,
        )(func)

    return decorator
