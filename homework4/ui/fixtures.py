import os
import allure
import pytest
from appium import webdriver
from ui.pages.base_page import BasePageANDROID
from ui.pages.main_page import MainPageANDROID
from ui.pages.settings_page import SettingsPageANDROID
from ui.pages.news_source_page import NewsSourcePageANDROID
from ui.pages.application_page import ApplicationPageANDROID
from ui.capability import capability_select


@pytest.fixture(scope='function')
def driver(config, test_dir):
    appium_url = config['appium']

    desired_caps = capability_select()
    driver = webdriver.Remote(appium_url, desired_capabilities=desired_caps)

    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def ui_report(driver, request, test_dir, config):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)


@pytest.fixture
def base_page(driver, config):
    return BasePageANDROID(driver=driver, config=config)


@pytest.fixture
def main_page(driver, config):
    return MainPageANDROID(driver=driver, config=config)


@pytest.fixture
def settings_page(driver, config):
    return SettingsPageANDROID(driver=driver, config=config)


@pytest.fixture
def news_source_page(driver, config):
    return NewsSourcePageANDROID(driver=driver, config=config)


@pytest.fixture
def application_page(driver, config):
    return ApplicationPageANDROID(driver=driver, config=config)
