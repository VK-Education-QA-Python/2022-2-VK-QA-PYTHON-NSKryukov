import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from ui.pages.login_page import LoginPage
from ui.pages.register_page import RegisterPage
from ui.pages.main_page import MainPage
from api.api_client import ApiClient


@pytest.fixture(scope='session')
def cookies(pre_creating_user):
    data = {
        'username': pre_creating_user['username'],
        'password': pre_creating_user['password'],
    }
    response = requests.post(url='http://localhost:8082/login', data=data, allow_redirects=False)
    cookies = response.cookies
    return str(cookies).split('=')[1].split(' ')[0]


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    url = config['url']
    selenoid = config['selenoid']
    vnc = config['vnc']
    headless = config['headless']
    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
    if selenoid:

        capabilities = {
            "browserName": "chrome",
            "browserVersion": "106.0",
            'goog:loggingPrefs': {'browser': 'ALL'},
            # "acceptInsecureCerts": True,
            # "acceptSslCerts": True,
            "selenoid:options": {
                "enableVNC": vnc,
                "additionalNetworks": ["application_test"]
            }
        }
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub/',
            desired_capabilities=capabilities
        )
    elif browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def register_page(driver):
    return RegisterPage(driver=driver)


@pytest.fixture()
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture(scope='function')
def api_client():
    return ApiClient()


@pytest.fixture(scope='session')
def mysql_client(request):
    client = request.config.mysql_client
    yield client
    client.connection.close()
