from typing import Any

import pytest
from pytest_case import case


@case("default", 1, 2, 3)
def test__add__single_simple_case(a, b, expected) -> None:
    assert expected == a + b


@case("first case", 1, 2, 3)
@case("second case", 2, 2, 4)
@case("third case", 3, 4, 7)
def test__add__multiple_arg_cases(a, b, expected) -> None:
    assert expected == a + b

@case("first case", 
    a=1,
    b=2,
    expected=3,
)
@case("second case", 
    a=5,
    b=6,
    expected=11,
)
def test__add__kwarg_params(a, b, expected) -> None:
    assert expected == a + b


@case("Explicit optional", 2, 4, 6)
@case("Implicit optional", 2, 3)
def test__add__with_optional(a, b, expected=5) -> None:
    assert expected == a + b


def test__case__too_many_parameters() -> None:
    def func(a: Any) -> None:
        pass

    with pytest.raises(TypeError):
        case("name", 1, 2)(func)


@case("")
def test__case__argvalue_priority__optional_param_default(a: int = 1, b: int = 2) -> None:
    assert 1 == a and 2 == b

@case("", 10)
def test__case__argvalue_priority__arg_override_default(a: int = 1, b: int = 2) -> None:
    assert 10 == a and 2 == b

@case("", a=2)
def test__case__argvalue_priority__kwarg_override_default(a: int = 1, b: int = 2) -> None:
    assert 2 == a and b == 2

@case("", 3, b=4)
def test__case__argvalue_priority__kwarg_override_arg(a: int = 1, b: int = 2) -> None:
    assert 3 == a and 4 == b
