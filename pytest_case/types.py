
from dataclasses import astuple, dataclass
from typing import Any, Callable, Dict, List, Tuple

import pytest


@dataclass
class UnwrappedFunc:
    unwrapped_func: Callable[[Any], Any]
    func_markers: List[pytest.MarkDecorator]
    ids: List[str]
    argnames: Tuple[str]
    argvalues: List[Tuple[Any]]
    defaults: Dict[str, Any]

    def __iter__(self):
        return iter(astuple(self))
