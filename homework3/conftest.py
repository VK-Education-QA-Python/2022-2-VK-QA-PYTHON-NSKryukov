import pytest

from client import ApiClient


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')

    if browser != 'chrome':
        raise RuntimeError(f'Unsupported browser: "{browser}"')

    return {
        'browser': browser,
    }


@pytest.fixture(scope='session')
def api_client(config):
    return ApiClient()
