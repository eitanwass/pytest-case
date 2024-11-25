# pytest-case

![workflow success](https://github.com/eitanwass/pytest-case/actions/workflows/pytest-case-ci.yml/badge.svg) [![codecov](https://codecov.io/github/eitanwass/pytest-case/graph/badge.svg?token=07NGAILDL2)](https://codecov.io/github/eitanwass/pytest-case) 

![PyPI - Downloads](https://img.shields.io/pypi/dm/pytest-case) [![PyPI - Version](https://img.shields.io/pypi/v/pytest-case)](https://pypi.org/project/pytest-case)


# Usage examples:

```python
import pytest
from typing import Tuple, Generator
from pytest_case import case


def add_test_cases() -> Generator[Tuple[int, int, int]]:
    yield (
        n
        for n in [
            (3, 3, 6),
            (3, 4, 7),
            (-1, 6, 5),
        ]
    )


@case("regular args", 4, 2, 2)
@case(
    "params as kwargs",
    a=2,
    b=2,
    expected=1,
)
@case('with expected fail', 1, 0, -1, mark=pytest.mark.xfail)
@case(add_test_cases())
def test__divide(a: int, b: int, expected: int) -> None:
    assert expected == a / b
```

# Features

## Default Arguments Values
```python
@case("Check for Failure", val="Failure")
@case("Check for success", val="Success", sanity="Success")
def test__with_default(val: str, sanity: str = "Failure") -> None:
    assert sanity == val
```

## Generator Case
```python
from itertools import product
from pytest_case import case

@case(product(
    ("Chrome", "Firefox", "Safari"), 
    ("Windows", "macOS", "Linux")
))
def test__browser_os_compatibility(browser: str, operating_system: str) -> None:
    # Will generate cases:
    # ("Chrome", "Windows"), ("Chrome", "macOS"), ("Chrome", "Linux"), ("Firefox", "Windows"), ...
    pass
```

## Using Fixtures
- Using pytest built-in `request` fixture.
    ```python
    def test__with_request_fixture(request: Any) -> None:
        fixture_value = request.getfixturevalue("fixture_name")
        ...
    ```
- Using [pytest-lazy-fixtures](https://github.com/dev-petrov/pytest-lazy-fixtures)
    ```python
    from pytest_case import case
    from pytest_lazy_fixtures import lf


    @case("Lazy Fixture Case", lf("fixture_name"))
    def test__with_lf_cases(fixture_val: Any) -> None
        ...
    ```

# Project Roadmap:
These are the the predicted checkpoints for this project:

- [x] **Test Arguments Default Values**
    That would be cool!
- [x] **Test Marks**
    Marks that are currently supported by pytest, such as: xfail, skip, ...
- [x] **Tests Cases Generators**
    Provide a generator function to the `case` to automatically generate cases.
- [x] **Use Fixtures**
    Use fixtures in cases and tests
- [ ] **Tests Samples Generation**
    Generate parameters to catch edge-cases, based on restrictions or datasets.
