import pytest
from pytest_case.utils.case_utils import is_case


@pytest.fixture
def func():
    def _func():
        pass
    return _func


def test__is_case__no_marks(func):
    assert not is_case(func)

def test__is_case__no_case_mark(func):
    func.pytestmark = [pytest.mark.skip]
    assert not is_case(func)

def test__is_case__with_case_mark(func):
    func.pytestmark = [pytest.mark.case]
    assert is_case(func)

def test__is_case__with_multiple_marks(func):
    func.pytestmark = [pytest.mark.skip, pytest.mark.case]
    assert is_case(func)

def test__is_case__with_case_mark_and_other_marks(func):
    func.pytestmark = [pytest.mark.case, pytest.mark.skip]
    assert is_case(func)
