import time
import allure
from ui.fixtures import *
import pytest
from base import BaseCase
from ui.fixtures import get_driver
from ui.pages.base_page import BasePage
from src.company_data import *


@pytest.fixture(scope='session')
def credentials():
    if sys.platform.startswith('win'):
        credentials = '..\\src\\credentials.txt'
    else:
        credentials = './src/credentials.txt'
    with open(credentials, 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
    return user, password


@pytest.fixture(scope='session')
def cookies(credentials, config):
    driver = get_driver(config['browser'], config['headless'], config['selenoid'],
                        config['vnc'], config['enable_video'])
    driver.get(config['url'])
    login_page = BasePage(driver)
    login_page.login(*credentials)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.mark.UI
class TestUI(BaseCase):
    @pytest.fixture()
    def file_path(self, repo_root):
        return os.path.join(repo_root, 'src', 'ad_picture.jpg')

    @allure.severity('critical')
    @allure.story('Creating campaign with objective - Traffic')
    def test_create_campaign(self, file_path, unique_name):
        self.main_page.go_to_create_campaign_page()
        self.create_campaign_page.create_campaign(link, ad_title, ad_body, file_path=file_path, name=unique_name)
        assert self.main_page.entity_is_added(unique_name)

    @allure.severity('critical')
    @allure.story('Creating audience with "Warface" data-source')
    def test_create_audience(self, unique_name):
        self.main_page.go_to_create_segment_page()
        self.create_segment_page.create_apps_and_games_segment(name=unique_name)
        assert self.main_page.entity_is_added(unique_name)

    @allure.severity('critical')
    @allure.story('Creating audience with "Vk education" group data-source')
    def test_create_vk_audience(self, unique_name):
        self.main_page.go_to_audiences_page()
        self.create_segment_page.create_vk_group_data()
        self.main_page.go_to_create_segment_page()
        self.create_segment_page.create_vk_group_segment(name=unique_name)
        assert self.main_page.entity_is_added(unique_name)
        self.main_page.delete_segment('title', unique_name)
        time.sleep(1)
        self.create_segment_page.delete_vk_group_data()
