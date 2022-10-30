import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.base_page import BasePageANDROID
from ui.pages.main_page import MainPageANDROID
from ui.pages.settings_page import SettingsPageANDROID
from ui.pages.news_source_page import NewsSourcePageANDROID
from ui.pages.application_page import ApplicationPageANDROID


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, ui_report):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePageANDROID = request.getfixturevalue('base_page')
        self.main_page: MainPageANDROID = request.getfixturevalue('main_page')
        self.settings_page: SettingsPageANDROID = request.getfixturevalue('settings_page')
        self.news_source_page: NewsSourcePageANDROID = request.getfixturevalue('news_source_page')
        self.application_page: ApplicationPageANDROID = request.getfixturevalue('application_page')

        self.logger.debug('Initial setup done!')
