import pytest
from ui.ui_base import RegisterBaseCase, LoginBaseCase
import faker
import allure
import time


faker = faker.Faker()


class TestLoginPage(LoginBaseCase):
    """
    This is a class of negative tests for login page.

    Starting page:
        Login page

    Tests steps:
        1. Trying to log in with random username or password
        2. Asserting that application shows a hint: "Invalid username or password" in login form

    Expected result:
        User did not log in and application shows an error: "Invalid username or password"
    """

    @pytest.mark.flaky()
    @pytest.mark.parametrize('field', ['username', 'password'])
    def test_negative_login_with_random_credentials(self, pre_creating_user, field):
        pre_creating_user[field] = faker.bothify('???????')
        self.login_page.login_user(pre_creating_user)
        alert_message = self.login_page.find(self.login_page.locators.HIDDEN_ALERT_FIELD).text
        with allure.step('Login user with random credentials'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert 'Invalid username or password' in alert_message


class TestRegisterExistingUser(RegisterBaseCase):

    @pytest.mark.flaky()
    def test_negative_creating_existing_user_by_username(self, random_user_data):
        """
        This is a negative test for register a user with existing username in DB.

        Starting page:
            Login page

        Test steps:
            1. Going to register page
            2. Trying to register user with existing in DB username and other info about user
            3. Asserting that application shows a hint: "User already exist" in register form

        Expected result:
            User did not sign in and application shows an error: "User already exist"
        """

        self.login_page.go_to_register_page()
        random_user_data['username'] = 'test_ui'
        self.register_page.register_user(random_user_data)
        time.sleep(1.5)
        with allure.step('Registred user with existing username'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        alert_message = self.register_page.find_without_waiting(self.register_page.locators.HIDDEN_ALERT_FIELD).text
        assert 'User already exist' in alert_message

    @allure.severity('Major')
    @pytest.mark.flaky()
    def test_negative_creating_existing_user_by_email(self, random_user_data):  # BUG
        """
          This is a negative test for register a user with existing email in DB.

          Starting page:
              Login page

          Test steps:
              1. Going to register page
              2. Trying to register user with existing in DB email and other info about user
              3. Asserting that application does not show a hint: "Internal Server Error" in register form

          Expected result:
              User did not sign in and application does not show an error: "Internal Server Error"
          """

        self.login_page.go_to_register_page()
        random_user_data['email'] = 'test_ui@mail.ru'
        self.register_page.register_user(random_user_data)
        time.sleep(1.5)
        with allure.step('Registred user with existing email'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        alert_message = self.register_page.find_without_waiting(self.register_page.locators.HIDDEN_ALERT_FIELD).text
        assert 'Internal Server Error' not in alert_message
