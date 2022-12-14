from ui.pages.base_page import BasePage
from ui.locators import basic_locators
import allure


class RegisterPage(BasePage):

    locators = basic_locators.RegisterPageLocators()
    url = 'http://app:8080/reg'

    @allure.step('Going to login page')
    def go_to_login(self):
        self.click_to_element(self.locators.LOGIN_BUTTON)

    def register_user(self, user_data):
        self.put_in_element(self.locators.NAME_FIELD, user_data['first_name'])
        self.put_in_element(self.locators.SURNAME_FIELD, user_data['last_name'])
        self.put_in_element(self.locators.MIDDLENAME_FIELD, user_data['middle_name'])
        self.put_in_element(self.locators.USERNAME_FIELD, user_data['username'])
        self.put_in_element(self.locators.EMAIL_FIELD, user_data['email'])
        self.put_in_element(self.locators.PASSWORD_FIELD, user_data['password'])
        self.put_in_element(self.locators.PASSWORD_FIELD_CONFIRM, user_data['password'])
        self.click_to_element(self.locators.CHECKBOX_BUTTON)
        with allure.step('Register user'):
            allure.attach(self.get_png_screenshot(), 'Completed register form', allure.attachment_type.PNG)
        self.click_to_element(self.locators.REGISTER_BUTTON)

    def register_user_without_checkbox(self, user_data):
        self.put_in_element(self.locators.NAME_FIELD, user_data['first_name'])
        self.put_in_element(self.locators.SURNAME_FIELD, user_data['last_name'])
        self.put_in_element(self.locators.MIDDLENAME_FIELD, user_data['middle_name'])
        self.put_in_element(self.locators.USERNAME_FIELD, user_data['username'])
        self.put_in_element(self.locators.EMAIL_FIELD, user_data['email'])
        self.put_in_element(self.locators.PASSWORD_FIELD, user_data['password'])
        self.put_in_element(self.locators.PASSWORD_FIELD_CONFIRM, user_data['password'])
        with allure.step('Register user without checkbox confirmation'):
            allure.attach(self.get_png_screenshot(), 'Completed register form', allure.attachment_type.PNG)
        self.click_to_element(self.locators.REGISTER_BUTTON)
