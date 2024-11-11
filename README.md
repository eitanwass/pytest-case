# pytest-case

```python
import pytest
from typing import Tuple, Generator
from pytest_case import case


def add_test_cases() -> Generator[Tuple[int, int, int], None]:
    return (
        n
        for n in [
            (3, 3, 6),
            (3, 4, 7),
            (-1, 6, 5),
        ]
    )


@case(1, 2, 3)
@case({
    "a": 2,
    "b": 2,
    "expected": "4",
})
@case('a', 1, pytest.mark.xfail)
@case(add_test_cases())
def test__add(a, b, expected) -> None:
    assert expected == a + b
```
