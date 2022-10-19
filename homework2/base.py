import os
import allure
import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.base_page import BasePage
from ui.pages.create_campaign_page import CreateCampaignPage
from ui.pages.main_page import MainPage
from ui.pages.create_segment_page import CreateSegmentPage


class BaseCase:
    driver = None
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def ui_report_log(self, driver, temp_dir):
        yield
        browser_logs = os.path.join(temp_dir, 'browser.log')
        with open(browser_logs, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
        with open(browser_logs, 'r') as f:
            allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.login_page = BasePage(driver)
        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.main_page = MainPage(driver)

        self.base_page: BasePage = (request.getfixturevalue('base_page'))
        self.create_campaign_page: CreateCampaignPage = (request.getfixturevalue('create_campaign_page'))
        self.create_segment_page: CreateSegmentPage = (request.getfixturevalue('create_segment_page'))
