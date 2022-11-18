import allure
import pytest
from base import BaseCase


class TestMarussiaAndroid(BaseCase):
    @allure.severity('Critical')
    @allure.story('Testing search in command line')
    @pytest.mark.AndroidUI
    def test_search_in_command_line(self):
        self.main_page.skip_preview()
        self.main_page.enter_command('Russia')
        self.main_page.find(self.main_page.locators.TEXT_CARD)
        self.main_page.swipe_and_click_to_surface_button()
        assert self.main_page.find(self.main_page.locators.FACT_TITLE_FIELD).text == '17125191 км²'

    @allure.severity('Critical')
    @allure.story('Testing calculator in command line')
    @pytest.mark.AndroidUI
    @pytest.mark.parametrize('test_input, result', [("13+12", "25"), ("10/2", "5")])
    def test_calculator_in_command_line(self, test_input, result):
        self.main_page.skip_preview()
        self.main_page.enter_command(test_input)
        assert self.main_page.check_answer(self.main_page.locators.DIALOG_ITEMS, result)

    @allure.severity('Critical')
    @allure.story('Testing changing news source')
    @pytest.mark.AndroidUI
    def test_changing_news_source(self):
        self.main_page.skip_preview()
        self.main_page.go_to_settings_menu()
        self.settings_page.go_to_news_source()
        self.news_source_page.setting_mail_ru_source()
        self.news_source_page.find(self.news_source_page.locators.CONFIRMATION_SIGN)
        self.news_source_page.go_to_main_page()
        self.main_page.enter_command('News')
        self.main_page.find(self.main_page.locators.NEWS_TRACK)

    @allure.severity('Critical')
    @allure.story('Testing apk information')
    @pytest.mark.AndroidUI
    def test_apk_information(self):
        self.main_page.skip_preview()
        self.main_page.go_to_settings_menu()
        self.settings_page.go_to_application_page()
        assert self.application_page.check_version()
        assert self.application_page.check_trademark()
