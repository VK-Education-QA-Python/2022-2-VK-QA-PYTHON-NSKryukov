from ui.pages.base_page import BasePageANDROID
from ui.locators.locators_android import NewsSourcePageANDROIDLocators
import allure


class NewsSourcePageANDROID(BasePageANDROID):
    locators = NewsSourcePageANDROIDLocators()

    @allure.step('Setting mail.ru news source')
    def setting_mail_ru_source(self):
        self.click(self.locators.MAIL_RU_NEWS_SOURCE)

    @allure.step('Going to main page')
    def go_to_main_page(self):
        self.driver.back()
        self.driver.back()
