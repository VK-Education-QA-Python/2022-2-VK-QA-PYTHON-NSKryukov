import time
import allure
import pytest
from base import BaseCase
from src.company_data import *


@pytest.mark.UI
class TestUI(BaseCase):
    """
    UI tests for https://target-sandbox.my.com/
    """

    @allure.severity('critical')
    @allure.story('Creating campaign with objective - Traffic')
    def test_create_campaign(self, file_path, unique_name):
        self.main_page.go_to_create_campaign_page()
        self.create_campaign_page.create_campaign(LINK, AD_TITLE, AD_BODY, file_path=file_path, name=unique_name)
        assert self.main_page.existing_of_campaign(unique_name)

    @allure.severity('critical')
    @allure.story('Creating audience with "Warface" data-source')
    def test_create_audience(self, unique_name):
        self.main_page.go_to_create_segment_page()
        self.create_segment_page.create_apps_and_games_segment(name=unique_name)
        assert self.create_segment_page.existing_of_segment(unique_name)

    @allure.severity('critical')
    @allure.story('Creating audience with "Vk education" group data-source')
    def test_create_vk_audience(self, unique_name):
        self.main_page.go_to_audiences_page()
        self.create_segment_page.create_vk_group_data()
        self.main_page.go_to_create_segment_page()
        self.create_segment_page.create_vk_group_segment(name=unique_name)
        assert self.create_segment_page.existing_of_segment(unique_name)
        self.create_segment_page.delete_segment(unique_name)
        time.sleep(1)
        self.create_segment_page.delete_vk_group_data()
