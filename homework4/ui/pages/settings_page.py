from ui.pages.base_page import BasePageANDROID
from ui.locators.locators_android import SettingsPageANDROIDLocators
import allure


class SettingsPageANDROID(BasePageANDROID):
    locators = SettingsPageANDROIDLocators()

    @allure.step('Going to news source page')
    def go_to_news_source(self):
        self.swipe_up_to_element(self.locators.NEWS_SOURCE_BUTTON, 4)
        self.click(self.locators.NEWS_SOURCE_BUTTON)

    @allure.step('Going to application page')
    def go_to_application_page(self):
        self.swipe_up_to_element(self.locators.ABOUT_APPLICATION_BUTTON, 5)
        self.click(self.locators.ABOUT_APPLICATION_BUTTON)
