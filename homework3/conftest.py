import pytest

from client import ApiClient


@pytest.fixture(scope='session')
def api_client():
    return ApiClient()
