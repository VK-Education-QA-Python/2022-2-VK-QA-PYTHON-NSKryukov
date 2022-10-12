import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption("--headless", action='store_true')


@pytest.fixture(scope='function')
def driver(request):
    if request.config.option.headless:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
    else:
        options = None
    driver = webdriver.Chrome(executable_path=ChromeDriverManager('105.0.5195.52').install(), options=options)
    driver.get('https://target-sandbox.my.com/')
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
