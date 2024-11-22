from __future__ import annotations

from functools import reduce
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Union, overload

import pytest
from _pytest.mark import ParameterSet

from pytest_case.consts import PYTEST_MARKER
from pytest_case.types import UnwrappedFunc
from pytest_case.utils.case_utils import is_case
from pytest_case.utils.func_utils import get_func_optional_params, get_func_param_names


__all__ = ["case"]


@overload
def case(cases_generator: Iterable[Any]) -> Callable[..., Any]: ...

@overload
def case(name: str, *args: Any, **kwargs: Any) -> Callable[..., Any]: ...


def wrap_func(
    argnames: Sequence[str],
    parameter_sets: Iterable[ParameterSet],
    defaults: Dict[str, Any],
) -> Callable[..., Callable[..., Any]]:
    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        We wrap the function with `pytest.mark.parametrize` with every case so it will exist in the last case.
        We unwrap the mark for every wrapped case.
        """
        return pytest.mark.parametrize(
            argnames=argnames,
            argvalues=parameter_sets,
        )(pytest.mark.case(defaults=defaults)(func))
    return wrapper


def unwrap_func(func: Callable[[Any], Any]) -> UnwrappedFunc:
    """
    Unwraps a case function into its original function and its pytest-case components.

    :param func: A function wrapped with `case`.
    :return: A dataclass containing the original function and its pytest-case arguments.
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


def _generator_case(gen: Iterable[Any], func: Callable[..., Any], **kwargs: Any) -> Callable[..., Any]:
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
    marks = kwargs.pop("marks", None) or tuple()

    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        # Can't check for `Iterable` because `str` is also iterable
        if not isinstance(name_or_gen, str):
            return _generator_case(name_or_gen, func, **kwargs)
        name = name_or_gen

        if not callable(func):
            raise TypeError(f"'{func}' is not a callable")
        func_params = get_func_param_names(func)
        if not len(func_params):
            raise TypeError("Test function does not take any parameters")
        if len(args) + len(kwargs) > len(func_params):
            # Too many args
            raise TypeError(
                f"Test '{func.__name__}' expected {len(func_params)} but case got {len(args) + len(kwargs)} params"
            )

        argnames = []
        defaults: Dict[str, Any] = {}
        case_parameter_sets: Iterable[ParameterSet] = []

        if is_case(func):
            # Wrapping another case
            unwrapped_func_attrs = unwrap_func(func)
            func = unwrapped_func_attrs.unwrapped_func
            argnames = unwrapped_func_attrs.argnames
            case_parameter_sets = unwrapped_func_attrs.argvalues
            defaults = unwrapped_func_attrs.defaults
        else:
            # If the wrapped function is a test function...
            func_params = get_func_param_names(func)
            defaults = get_func_optional_params(func)
            func_required_params = func_params[:len(func_params) - len(defaults)]
            # All the rest should be fixtures or will raise an error because tey are not provided
            argnames = (*func_required_params, *defaults.keys())

            if "marks" in argnames:
                raise TypeError("Function parameters cannot contain reserved keyword 'marks'")
        
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

        case_parameter_sets = [pytest.param(*case_argvalues, marks=marks, id=name)] + case_parameter_sets

        return wrap_func(
            argnames=argnames,
            parameter_sets=case_parameter_sets,
            defaults=defaults,
        )(func)
    
    return decorator
