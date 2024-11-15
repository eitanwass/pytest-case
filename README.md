# pytest-case

```python
import pytest
from typing import Tuple, Generator
from pytest_case import case


def add_test_cases() -> Generator[Tuple[int, int, int], None]:
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


# Project Roadmap:
These are the the predicted checkpoints for this project:

- **Test Marks**
    Marks that are currently supported by pytest, such as: xfail, skip, ...
- **Tests Cases Generators**
    Provide a generator function to the `case` to automatically generate cases.
- **Tests Samples Generation**
    Generate parameters to catch edge-cases, based on restrictions or datasets.
