import os
import faker
import pytest
from fixtures import *
from database.mysql_client import MysqlClient


faker = faker.Faker()


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='function')
def random_user_data():

    return {'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'middle_name': faker.first_name() + 'mid',
            'username': faker.bothify('??????????'),
            'email': faker.email(),
            'password': '123456'
            }


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default='http://app:8080')
    parser.addoption('--headless', action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')
    headless = request.config.getoption('--headless')
    if request.config.getoption('--selenoid'):
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
        selenoid = 'http://127.0.0.1:4444/wd/hub'
    else:
        selenoid = None
        vnc = False

    return {
        'browser': browser,
        'url': url,
        'headless': headless,
        'selenoid': selenoid,
        'vnc': vnc,
    }


def pytest_configure(config):
    mysql_client = MysqlClient(user='root', password='0000', db_name='vkeducation')
    mysql_client.connect()
    config.mysql_client = mysql_client
