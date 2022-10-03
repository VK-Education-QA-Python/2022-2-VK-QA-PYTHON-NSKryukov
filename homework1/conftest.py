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
    wait_time = 7
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    driver.get('https://target-sandbox.my.com/')
    driver.maximize_window()
    driver.implicitly_wait(wait_time)
    yield driver
    driver.quit()
