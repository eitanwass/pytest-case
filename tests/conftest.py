
import pytest


@pytest.fixture
def lazy_fixture_val() -> str:
    return "lazy_fixture"


@pytest.fixture
def requested_fixture() -> str:
    return "request_val"
