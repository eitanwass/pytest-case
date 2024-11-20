# pytest-case

![workflow success](https://github.com/eitanwass/pytest-case/actions/workflows/pytest-case-ci-cd.yml/badge.svg) [![codecov](https://codecov.io/github/eitanwass/pytest-case/graph/badge.svg?token=07NGAILDL2)](https://codecov.io/github/eitanwass/pytest-case) 

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
@case('with expected fail', 1, 0, mark=pytest.mark.xfail)
@case(add_test_cases())
def test__divide(a, b, expected) -> None:
    assert expected == a / b
```

# Features

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

# Project Roadmap:
These are the the predicted checkpoints for this project:

- [ ] **Test Marks**
    Marks that are currently supported by pytest, such as: xfail, skip, ...
- [x] **Tests Cases Generators**
    Provide a generator function to the `case` to automatically generate cases.
- [ ] **Tests Samples Generation**
    Generate parameters to catch edge-cases, based on restrictions or datasets.
