from ui.locators import basic_locators
from ui.pages.base_page import BasePage
import allure
from selenium.common.exceptions import TimeoutException


class MainPage(BasePage):
    locators = basic_locators.MainPageLocators()
    url = 'https://target-sandbox.my.com/dashboard'

    @allure.step('Going to creating company page')
    def go_to_create_campaign_page(self):
        try:
            self.find(self.locators.CREATE_CAMPAIGN_BUTTON, timeout=20).click()
        except TimeoutException:
            self.find(self.locators.CREATE_CAMPAIGN_BUTTON_PRIMARY).click()

    @allure.step('Going to creating segment page')
    def go_to_create_segment_page(self):
        self.find(self.locators.AUDIENCES_MODULE, timeout=60).click()
        try:
            self.find(self.locators.CREATE_AUDIENCE_BUTTON, timeout=10).click()
        except TimeoutException:
            self.find(self.locators.CREATE_AUDIENCE_BUTTON_PRIMARY).click()

    @allure.step('Going to audiences page')
    def go_to_audiences_page(self):
        self.find(self.locators.AUDIENCES_MODULE, timeout=30).click()

    def existing_of_campaign(self, name):
        self.put_in_element(self.locators.COMPANY_SEARCH_INPUT, name)
        self.find(self.locators.SELECT_ALL_BUTTON).click()
        element = self.find(self.locators.ELEMENTS_CAMPAIGNS_LIST)
        return element.get_attribute('title') == name
