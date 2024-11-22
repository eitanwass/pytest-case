
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple

import pytest
from _pytest.mark import ParameterSet


@dataclass
class UnwrappedFunc:
    unwrapped_func: Callable[[Any], Any]
    func_markers: List[pytest.MarkDecorator]

    argnames: Tuple[str]
    argvalues: List[ParameterSet]

    defaults: Dict[str, Any]
