from itertools import product
from typing import Any

import pytest
from pytest_case import case

from pytest_lazy_fixtures import lf


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


@case("Another implicit optional", 1, 4)
@case("Explicit optional", 2, 4, 6)
@case("Implicit optional", 2, 3)
def test__add__with_optional(a, b, expected=5) -> None:
    print(a, b, expected)
    assert expected == a + b


def test__case__too_many_parameters() -> None:
    def func(a: Any) -> None:
        pass

    with pytest.raises(TypeError):
        case("name", 1, 2)(func)


def test__case__reserved_kw_marks() -> None:
    def func(marks: Any) -> None:
        pass

    with pytest.raises(TypeError):
        case("name", 1)(func)


@case("optional_param_default")
def test__case__argvalue_priority__optional_param_default(a: int = 1, b: int = 2) -> None:
    assert 1 == a and 2 == b

@case("arg_override_default", 10)
def test__case__argvalue_priority__arg_override_default(a: int = 1, b: int = 2) -> None:
    assert 10 == a and 2 == b

@case("kwarg_override_default", a=2)
def test__case__argvalue_priority__kwarg_override_default(a: int = 1, b: int = 2) -> None:
    assert 2 == a and b == 2

@case("kwarg_override_arg", 3, b=4)
def test__case__argvalue_priority__kwarg_override_arg(a: int = 1, b: int = 2) -> None:
    assert 3 == a and 4 == b

@case(((x, x ** 2) for x in range(10)), name="{} ** 2 == {}")
def test__case__generator(a, b) -> None:
    assert a ** 2 == b

@case(product(("a", "b"), ("1", "2")), name="({}, {})")
def test__case__product(a, b) -> None:
    assert a in ("a", "b") and b in ("1", "2")

@case("should pass", 1)
@case("should skip", 2, marks=pytest.mark.skip)
@case("should fail", -1, marks=pytest.mark.xfail(reason="This number is negative"))
def test__case__marking(a: int) -> None:
    assert a > 0


@case("with lazy fixture", lf("lazy_fixture_val"))
def test__case__with_fixture(lazy_fix: str) -> None:
    assert "lazy_fixture" == lazy_fix


def test__case__with_request(request: Any) -> None:
    used_fixture = request.getfixturevalue("requested_fixture")
    assert "request_val" == used_fixture
