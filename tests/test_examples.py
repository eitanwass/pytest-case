from pytest_case import case


@case("default", 1, 2, 3)
def test__add__single_case(a, b, expected) -> None:
    assert expected == a + b


@case("first case", 1, 2, 3)
@case("second case", 2, 2, 4)
@case("third case", 3, 4, 7)
def test__add_two_cases(a, b, expected) -> None:
    assert expected == a + b
