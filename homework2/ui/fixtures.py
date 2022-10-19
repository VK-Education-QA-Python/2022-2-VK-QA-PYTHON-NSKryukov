import os
import shutil
import sys
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from ui.pages.base_page import BasePage
from ui.pages.create_campaign_page import CreateCampaignPage
from ui.pages.create_segment_page import CreateSegmentPage


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


@pytest.fixture()
def driver(config, temp_dir):
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
    elif browser == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


def get_driver(browser_name, headless=False, selenoid=False, vnc=False, enable_video=False):
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
        browser = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )
    elif browser_name == 'chrome':
        browser = webdriver.Chrome(executable_path=ChromeDriverManager('105.0.5195.52').install(), options=options)
    elif browser_name == 'firefox':
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser_name}"')
    browser.maximize_window()
    return browser


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def create_campaign_page(driver):
    return CreateCampaignPage(driver=driver)


@pytest.fixture
def create_segment_page(driver):
    return CreateSegmentPage(driver=driver)
