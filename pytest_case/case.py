from __future__ import annotations

from collections import defaultdict, namedtuple
from operator import itemgetter
from typing import Any, Callable, Dict, Iterable, List, Sequence, Tuple

import pytest


CASE_MARKER = "pytest_case"
PYTEST_MARKER = "pytestmark"


def _is_case(func: Callable[[Any], Any]) -> bool:
    return getattr(func, CASE_MARKER, False)


def _extract_case_params(func: Callable[[Any], Any]) -> Tuple[List[str], Tuple[Any], List[Tuple[Any]]]:
    # Assumming func is a case
    extracted_mark = next(
        (
            mark
            for mark in getattr(func, PYTEST_MARKER)
            if mark.name == "parametrize"
        ),
        None
    )

    return itemgetter("ids", "argnames", "argvalues")(extracted_mark.kwargs)


def wrap_func(
    ids: Sequence[str],     # TODO: Support dynamic func IDs
    argnames: Sequence[str],
    argvalues: Iterable[Sequence[object]],
) -> Callable[[Any], Any]:
    def wrapper(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        """
        We wrap the function with `pytest.mark.parametrize` with every case so it will exist in the last case.
        We unwrap the mark for every wrapped case.
        """
        parametrized_func = pytest.mark.parametrize(
            ids=ids,
            argnames=argnames,
            argvalues=argvalues,
        )(func)

        setattr(parametrized_func, "pytest_case", True)

        return parametrized_func
    return wrapper


def unwrap_func(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    delattr(func, PYTEST_MARKER)
    return func


def get_func_param_names(func: Callable[[Any], Any]) -> Tuple[str, ...]:
    func_code = func.__code__
    func_arg_count = func_code.co_argcount
    return func_code.co_varnames[:func_arg_count]


def get_func_optional_params(func: Callable[[Any], Any]) -> Dict[str, Any]:
    func_params = get_func_param_names(func)
    return dict(
        reversed(list(
            zip(
                reversed(func_params),
                reversed(func.__defaults__ or [])
                )
            ))
        )


def case(name: str, *args: Any, **kwargs: Any) -> Callable[[Any], Any]:
    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        ids = []

        argnames = []
        func_optional_params: Dict[str, Any] = {}
        args_dict = defaultdict(tuple)

        if not _is_case(func):
            all_func_params = get_func_param_names(func)

            if len(args) + len(kwargs) > len(all_func_params):
                # Too many args
                raise TypeError(
                    f"Test '{func.__name__}' expected {len(all_func_params)} but case got {len(args) + len(kwargs)} params"
                )
            
            func_optional_params = get_func_optional_params(func)
            func.__defaults__ = None
            func_required_params = all_func_params[:len(all_func_params) - len(func_optional_params or [])]
            # All the rest should be fixtures or will raise an error because tey are not provided

            argnames = (*func_required_params, *func_optional_params.keys())
        else:
            ids, argnames, argvalues = _extract_case_params(func)
            args_dict = dict(zip(argnames, list(zip(*argvalues))))
            func = unwrap_func(func)
            func_optional_params = get_func_optional_params(func)

        ids = [name] + ids

        for arg_index, argname in enumerate(argnames):
            new_argvalue = None

            if argname in func_optional_params:
                # Has default value - use it
                new_argvalue = func_optional_params[argname]
            
            if arg_index < len(args):
                # Provided in args - use it
                new_argvalue = args[arg_index]

            if argname in kwargs:
                # Provided in kwargs - use it
                new_argvalue = kwargs[argname]

            if new_argvalue is None:
                # Should never happen.
                raise TypeError("Something weird has happened...")

            args_dict[argname] += (new_argvalue, )

        return wrap_func(
            ids=ids,
            argnames=list(args_dict.keys()),
            argvalues=list(zip(*args_dict.values())),
        )(func)
    
    return decorator
