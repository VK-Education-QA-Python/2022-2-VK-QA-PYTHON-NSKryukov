from ui.pages.base_page import BasePage
from ui.locators import basic_locators
import allure


class LoginPage(BasePage):

    locators = basic_locators.LoginPageLocators()
    url = 'http://app:8080/'

    @allure.step('Going to register page')
    def go_to_register_page(self):
        self.click_to_element(self.locators.REGISTER_BUTTON)

    def login_user(self, credentials):
        self.put_in_element(self.locators.USERNAME_FIELD, credentials['username'])
        self.put_in_element(self.locators.PASSWORD_FIELD, credentials['password'])
        with allure.step('Logining user'):
            allure.attach(self.get_png_screenshot(), 'Completed login form', allure.attachment_type.PNG)
        self.click_to_element(self.locators.LOGIN_BUTTON)
