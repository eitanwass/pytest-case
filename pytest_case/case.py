from __future__ import annotations

from collections import namedtuple
from typing import Any, Callable

import pytest


class PytestCase(object):
    cases = []
    test_func = None

    @classmethod
    def case(cls, name: str, *args: Any, **kwargs: Any) -> Callable[[Any], Any]:
        def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            cls.cases.append((name, args, kwargs))

            if hasattr(func, "pytestmark"):
                # Remove pytest mark
                delattr(func, "pytestmark")

            func_obj = func.__code__
            argnames = func_obj.co_varnames[:func_obj.co_argcount]
            argvalues = []

            ids = []

            case_cls = namedtuple("Case", argnames)

            for index, (name_, args_, kwargs_) in enumerate(reversed(cls.cases)):
                # TODO: handle defaults
                ids.append(name_ or str(index))
                argvalues.append(tuple(case_cls(*args_, **kwargs_)))

            print("ids", ids)
            print("argnames", argnames)
            print("argvalues", argvalues)

            return pytest.mark.parametrize(
                argnames=argnames,
                argvalues=argvalues,
                ids=ids
            )(func)
        
        return decorator
