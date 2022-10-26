import os
import shutil
import sys
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ui.pages.base_page import BasePage
from ui.pages.create_campaign_page import CreateCampaignPage
from ui.pages.create_segment_page import CreateSegmentPage


@pytest.fixture(scope='session')
def credentials(repo_root):
    if sys.platform.startswith('win'):
        credentials = os.path.join(repo_root, 'src\credentials.txt')
    else:
        credentials = os.path.join(repo_root, 'src/credentials.txt')
    with open(credentials, 'r') as file:
        user = file.readline().strip()
        password = file.readline().strip()
    return user, password


@pytest.fixture(scope='session')
def cookies(credentials, config, driver_authorization):
    driver = driver_authorization
    driver.get(config['url'])
    login_page = BasePage(driver)
    login_page.login(*credentials)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


def driver_initialising(config):
    browser = config['browser']
    url = config['url']
    selenoid = config['selenoid']
    vnc = config['vnc']
    enable_video = config['enable_video']
    headless = config['headless']
    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
    if selenoid:
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "105.0",
            "selenoid:options": {
                "enableVNC": vnc,
                "enableVideo": enable_video
            }
        }
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )
    elif browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager('105.0.5195.52').install(), options=options)
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    return driver


@pytest.fixture(scope='function')
def driver(config):
    driver = driver_initialising(config)
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def driver_authorization(config):
    driver = driver_initialising(config)
    yield driver


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def create_campaign_page(driver):
    return CreateCampaignPage(driver=driver)


@pytest.fixture
def create_segment_page(driver):
    return CreateSegmentPage(driver=driver)
