import time
import pytest
from ui.ui_base import *
from database.db_base import *
import faker
from ui.locators.basic_locators import RegisterPageLocators
import allure

faker = faker.Faker()


class TestPositiveRegistration(RegisterBaseCase):
    """
    This is a class of positive tests for register page.

    Starting page:
        Login page

    Tests steps:
        1. Going to register page
        2. Trying to register user
        3. Asserting that current url equals main page url

    Expected result:
        User successfully signed up and was redirected to main page
    """

    def test_positive_registration(self, random_user_data):
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Register user'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    def test_positive_registration_without_middle_name(self, random_user_data):
        random_user_data['middle_name'] = ''
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Register user without middlename'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url


class TestNegativeRegistrationWithoutOneField(RegisterBaseCase):
    """
    This is a class of negative tests for register page.
    Checking register process without one filled in field except middle name.

    Starting page:
        Login page

    Tests steps:
        1. Going to register page
        2. Trying to register user without one field
        3. Asserting that current url equals register page url

    Expected result:
        User did not sign up and was redirected to register page
    """

    def test_negative_registration_without_name(self, random_user_data):
        random_user_data['first_name'] = ''
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user without name'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.register_page.url

    def test_negative_registration_without_surname(self, random_user_data):
        self.login_page.go_to_register_page()
        random_user_data['last_name'] = ''
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user without surname'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.register_page.url

    def test_negative_registration_without_username(self, random_user_data):
        random_user_data['username'] = ''
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user without username'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.register_page.url

    def test_negative_registration_without_email(self, random_user_data):
        random_user_data['email'] = ''
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user without email'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.register_page.url

    def test_negative_registration_without_password(self, random_user_data):
        random_user_data['password'] = ''
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user without password'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.register_page.url

    def test_negative_registration_without_checkbox(self, random_user_data):
        self.login_page.go_to_register_page()
        self.register_page.register_user_without_checkbox(random_user_data)
        with allure.step('Registred user without checkbox confirmation'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.register_page.url


class TestPositiveRegistrationWithEdgeLengths(RegisterBaseCase):
    """
    This is a class of positive tests for register page.
    Checking register process with min or max length of value filled in form according to html attributes.

    Starting page:
        Login page

    Tests steps:
        1. Going to register page
        2. Trying to register user with max or min length of value
        3. Asserting that current url equals main page url

    Expected result:
        User successfully signed up and was redirected to main page
    """

    def test_positive_registration_min_name_length(self, random_user_data):
        random_user_data['first_name'] = faker.bothify('?')
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with 1 symbol in name field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    def test_positive_registration_max_name_length(self, random_user_data):
        random_user_data['first_name'] = faker.bothify('?') * 45
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with max symbols in name field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    def test_positive_registration_min_surname_length(self, random_user_data):
        random_user_data['last_name'] = faker.bothify('?')
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with 1 symbol in surname field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    @allure.severity('Minor')
    def test_positive_registration_max_surname_length(self, random_user_data):  # BUG
        random_user_data['last_name'] = faker.bothify('?') * 300
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with max symbols in surname field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    def test_positive_registration_min_middle_name_length(self, random_user_data):
        random_user_data['middle_name'] = faker.bothify('?')
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with 1 symbol in middle_name field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    @allure.severity('Minor')
    def test_positive_registration_max_middle_name_length(self, random_user_data):  # BUG
        random_user_data['middle_name'] = faker.bothify('?') * 300
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with max symbols in middle_name field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url != self.main_page.url

    def test_positive_registration_min_username_length(self, random_user_data):
        random_user_data['username'] = faker.bothify('??????')
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with 1 symbol in username field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    def test_positive_registration_max_username_length(self, random_user_data):
        random_user_data['username'] = faker.bothify('?') * 16
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with max symbols in username field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    def test_positive_registration_min_email_length(self, random_user_data):
        random_user_data['email'] = faker.bothify('?') + '@example.com'
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with min symbols in email field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    @allure.severity('Minor')
    def test_positive_registration_max_email_length(self, random_user_data):
        random_user_data['email'] = f'{faker.bothify("????") * 13}@mail.ru'
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        time.sleep(4)
        with allure.step('Registred user with max symbols in email field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    @allure.severity('Minor')
    def test_positive_registration_min_password_length(self, random_user_data):
        random_user_data['password'] = faker.bothify('?')
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with 1 symbol in password field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    @allure.severity('Minor')
    def test_positive_registration_max_password_length(self, random_user_data):  # BUG
        random_user_data['password'] = faker.bothify('??') * 150
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with max symbols in password field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url


class TestRegistrationFormPlaceholders(RegisterBaseCase):
    """
    This is a class of tests that checking placeholders in register form.

    Starting page:
        Login page

    Tests steps:
        1. Going to register page
        2. Getting placeholder value of field in register form
        3. Asserting that placeholder value written correctly

    Expected result:
        Placeholder value of element written correctly
    """

    locators_matching = {
        'Name': RegisterPageLocators.NAME_FIELD,
        'Surname': RegisterPageLocators.SURNAME_FIELD,
        'Middlename': RegisterPageLocators.MIDDLENAME_FIELD,
        'Username': RegisterPageLocators.USERNAME_FIELD,
        'Email': RegisterPageLocators.EMAIL_FIELD,
        'Password': RegisterPageLocators.PASSWORD_FIELD,
        'Repeat password': RegisterPageLocators.PASSWORD_FIELD_CONFIRM
    }

    @allure.severity('Minor')
    @pytest.mark.parametrize("test_input",
                             ['Name', 'Surname', 'Middlename', 'Username', 'Email', 'Password',
                              'Repeat password'])  # BUG
    def test_name_placeholder(self, test_input):
        self.login_page.go_to_register_page()
        element = self.register_page.find(self.locators_matching[test_input])
        placeholder_value = element.get_attribute("placeholder")
        with allure.step('Checking register page'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert placeholder_value == test_input


class TestRegisterNegativeEmailField(RegisterBaseCase):
    """
    This is a class of negative tests for register page.
    Checking features of ways to write email.

    Starting page:
        Login page

    Tests steps:
        1. Going to register page
        2. Trying to register with invalid email value ( with only domain name or without domain name )
        3. Asserting that application shows an error "Invalid email address"

    Expected result:
        Application shows a hint "Invalid email address"
    """

    def test_negative_email_value_first(self, random_user_data):
        self.login_page.go_to_register_page()
        random_user_data['email'] = '@gmail.com'
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with invalid email value'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        alert_message = self.register_page.find(self.register_page.locators.HIDDEN_ALERT_FIELD).text
        assert 'Invalid email address' in alert_message

    def test_negative_email_value_second(self, random_user_data):
        self.login_page.go_to_register_page()
        random_user_data['email'] = faker.bothify('?????????')
        self.register_page.register_user(random_user_data)
        with allure.step('Registred user with invalid email value'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        alert_message = self.register_page.find(self.register_page.locators.HIDDEN_ALERT_FIELD).text
        assert 'Invalid email address' in alert_message


class TestRegisterNegativeSpecialSymbolsInFields(RegisterBaseCase):
    """
    This is a class of negative tests for register page.
    Checking application reaction to special symbols in name/surname/middlename/email.

    Starting page:
        Login page

    Tests steps:
        1. Going to register page
        2. Trying to register with special symbols in name/surname/middlename/email fields
        3. Asserting that current url equals to register page url

    Expected result:
        User did not sign up and was redirected to register pag
    """

    @allure.severity('Major')
    @pytest.mark.parametrize('field', ['first_name', 'last_name', 'middle_name', 'email'])  # everything BUG
    def test_negative_putting_special_symbols(self, random_user_data, field):
        random_user_data[field] = faker.bothify('??????') + '#$%^/'
        if field == 'email':
            random_user_data[field] = faker.bothify('??????') + '%^&' + '@example.ru'
        self.login_page.go_to_register_page()
        self.register_page.register_user(random_user_data)
        with allure.step(f'Registred user with special symbols in {field} field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.register_page.url


class TestLoginPage(LoginBaseCase):

    def test_positive_login_user(self, pre_creating_user):
        """
         Positive test for login user. Checking user login process.

         Starting page:
             Login page

         Tests steps:
             1. Trying to log in with credentials of existing user
             2. Asserting that current url equals to main page url

         Expected result:
             User successfully logged in and was redirected in main page
         """

        self.login_page.login_user(pre_creating_user)
        with allure.step('Logged user'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    @pytest.mark.parametrize('field', ['username', 'password'])
    def test_negative_login_without_field(self, pre_creating_user, field):
        """
         Negative test for login user.
         Checking login process without filling one field.

         Starting page:
             Login page

         Tests steps:
             1. Trying to log in without filling one field
             2. Asserting that current url equals to login page url

         Expected result:
             User did not log in and was redirected to login page
         """

        pre_creating_user[field] = ''
        self.login_page.login_user(pre_creating_user)
        with allure.step(f'Logged user without {field} field'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.login_page.url


class TestPositiveLoginFieldsEdgeLengths(LoginBaseCase):
    """
    This is a class of positive tests for login page.
    Checking login process with min or max length of value filled in form.

    Starting page:
        Login page

    Tests steps:
        1. Trying to log in user with max or min length of value
        2. Asserting that current url equals main page url

    Expected result:
        User successfully logged in and was redirected to main page
    """

    def test_positive_login_min_username_length(self):
        credentials = {'username': 'testqa', 'password': '123456'}
        self.login_page.login_user(credentials)
        with allure.step('Logged user with min username length'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    def test_positive_login_max_username_length(self):
        credentials = {'username': 'testqatestqatest', 'password': '123456'}
        self.login_page.login_user(credentials)
        with allure.step('Logged user with max username length'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    def test_positive_login_min_password_length(self):
        credentials = {'username': 'qatesting', 'password': 'g'}
        self.login_page.login_user(credentials)
        with allure.step('Logged user with min password length'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    def test_positive_login_max_password_length(self):
        password = '12' * 127 + 'p'
        credentials = {'username': 'testingqa', 'password': password}
        self.login_page.login_user(credentials)
        with allure.step('Logged user with max password length'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url


class TestMainPageCorrectlyDisplaying(UIBaseCase):
    """
    This is a class of tests for correctly displaying elements in main page.

    Starting page:
        Main page

    Tests steps:
        1. Asserting that some element is presented in main page

    Expected result:
        Element is presented in main page
    """

    def test_hint_in_footer(self):
        with allure.step('Checking footer hint in main page'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.main_page.find(self.main_page.locators.HINT_FIELD).text

    def test_username_is_correctly_displayed(self, pre_creating_user):
        username_string = self.main_page.find(self.main_page.locators.USERNAME_STRING).text
        expected_username = pre_creating_user['username']
        with allure.step('Checking username in main page'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert expected_username in username_string

    def test_vk_id_is_showed(self):
        with allure.step('Checking vk id is showing in main page'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.main_page.find(self.main_page.locators.VK_ID_STRING)


class TestMainPageHeaderButtons(UIBaseCase):
    def test_logout(self):
        """
        This test checks logout button in main page.

        Starting page:
            Main page

        Test steps:
            1. Clicking to log out button in page header
            2. Asserting that current url equals to login page url

        Expected result:
            User successfully logged out
        """

        self.main_page.click_to_element(self.main_page.locators.LOGOUT_BUTTON)
        with allure.step('Clicked to logout button in main page'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.login_page.url + 'login'

    def test_home_button(self):
        """
        This test checks home button in main page.

        Starting page:
            Main page

        Test steps:
            1. Clicking to home button in page header
            2. Asserting that current url equals to main page url

        Expected result:
            User stayed in main page
        """

        self.main_page.click_to_element(self.main_page.locators.HOME_BUTTON)
        with allure.step('Clicked to home button in main page'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    def test_app_button(self):
        """
        This test checks app button ( with bug picture ) in main page.

        Starting page:
            Main page

        Test steps:
            1. Clicking to app button in page header
            2. Asserting that current url equals to main page url

        Expected result:
            User stayed in main page
        """

        with allure.step('Clicked to app button in main page'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        self.main_page.click_to_element(self.main_page.locators.APP_BUTTON)
        assert self.driver.current_url == self.main_page.url

    @allure.severity('Minor')
    @pytest.mark.parametrize('index', [0, 1, 2])  # BUG
    def test_click_to_header_button(self, index):
        """
           This test checks "Linux"/"Python"/"Network" button in main page header in main page.

           Starting page:
               Main page

           Test steps:
               1. Clicking to "Linux"/"Python"/"Network" button in main page header
               2. Asserting that current url equals to main page url

           Expected result:
               User stayed in main page
        """

        elem = self.main_page.find_elements_list(self.main_page.locators.HEADER_BUTTONS)[index]
        self.main_page.click_to_element(elem)
        with allure.step('Clicked to button in header of main page'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url

    @allure.severity('Minor')
    def test_popup_menu_first_link_python(self):  # BUG
        """
           This test checks "Python history" button in popup menu in main page header.

           Starting page:
               Main page

           Test steps:
               1. Moving cursor to "Python" field in header
               2. Clicking to "Python history" button in popup menu
               3. Moving to nex tab
               4. Asserting "Python" in tab title

           Expected result:
               Opened new tab with "Python" in tab title
        """

        button = self.main_page.find_elements_list(self.main_page.locators.HEADER_BUTTONS)[0]
        self.main_page.move_to_element(button)
        self.main_page.click_to_element(self.main_page.locators.HIDDEN_PYTHON_LINK)
        with allure.step('Clicked to Python button in popup menu'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url
        self.driver.switch_to.window(self.driver.window_handles[1])
        with allure.step('Switched to next tab'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert 'Python' in self.driver.title

    def test_popup_menu_second_link_python(self):
        """
           This test checks "Flask" button in popup menu in main page header.

           Starting page:
               Main page

           Test steps:
               1. Moving cursor to "Python" field in header
               2. Clicking to "Flask" button in popup menu
               3. Moving to nex tab
               4. Asserting "Flask" in tab title

           Expected result:
               Opened new tab with "Flask" in tab title
        """

        button = self.main_page.find_elements_list(self.main_page.locators.HEADER_BUTTONS)[0]
        self.main_page.move_to_element(button)
        self.main_page.click_to_element(self.main_page.locators.HIDDEN_FLASK_LINK)
        with allure.step('Clicked to Flask button in popup menu'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url
        self.driver.switch_to.window(self.driver.window_handles[1])
        with allure.step('Switched to next tab'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert 'Flask' in self.driver.title

    @allure.severity('Minor')
    def test_popup_menu_link_linux(self):  # BUG
        """
           This test checks "Centos" button in popup menu in main page header.

           Starting page:
               Main page

           Test steps:
               1. Moving cursor to "Linux" field in header
               2. Clicking to "Download Centos" button in popup menu
               3. Moving to nex tab
               4. Asserting "Centos" in tab title

           Expected result:
               Opened new tab with "Centos" in tab title
        """

        button = self.main_page.find_elements_list(self.main_page.locators.HEADER_BUTTONS)[1]
        self.main_page.move_to_element(button)
        self.main_page.click_to_element(self.main_page.locators.HIDDEN_CENTOS_LINK)
        with allure.step('Clicked to Centos button in popup menu'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url
        self.driver.switch_to.window(self.driver.window_handles[1])
        with allure.step('Switched to next tab'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert 'Centos' in self.driver.title

    def test_popup_menu_link_wireshark_news(self):
        """
           This test checks "Wireshark news" href in popup menu in main page header.

           Starting page:
               Main page

           Test steps:
               1. Moving cursor to "Network" field in header
               2. Finding element "Wireshark news"
               3. Asserting "https://www.wireshark.org/news/" equals href value of element found in step 2

           Expected result:
               Href value equals to "https://www.wireshark.org/news/"
        """

        button = self.main_page.find_elements_list(self.main_page.locators.HEADER_BUTTONS)[2]
        self.main_page.move_to_element(button)
        href_value = self.main_page.find(self.main_page.locators.HIDDEN_WIRESHARK_NEWS_BUTTON).get_attribute('href')
        assert 'https://www.wireshark.org/news/' == href_value

    def test_popup_menu_link_wireshark_download(self):
        """
           This test checks "Wireshark download" href in popup menu in main page header.

           Starting page:
               Main page

           Test steps:
               1. Moving cursor to "Network" field in header
               2. Finding element "Wireshark download"
               3. Asserting "https://www.wireshark.org/#download" equals href value of element found in step 2

           Expected result:
               Href value equals to "https://www.wireshark.org/#download"
        """

        button = self.main_page.find_elements_list(self.main_page.locators.HEADER_BUTTONS)[2]
        self.main_page.move_to_element(button)
        href_value = self.main_page.find(self.main_page.locators.HIDDEN_WIRESHARK_DOWNLOAD_BUTTON).get_attribute('href')
        assert 'https://www.wireshark.org/#download' == href_value

    def test_popup_menu_link_tcpdump_examples(self):
        """
           This test checks "Tcpdump" button in popup menu in main page header.

           Starting page:
               Main page

           Test steps:
               1. Moving cursor to "Network" field in header
               2. Clicking to "Tcpdump" button in popup menu
               3. Moving to nex tab
               4. Asserting "Tcpdump Examples" in tab title

           Expected result:
               Opened new tab with "Tcpdump Examples" in tab title
        """

        button = self.main_page.find_elements_list(self.main_page.locators.HEADER_BUTTONS)[2]
        self.main_page.move_to_element(button)
        self.main_page.click_to_element(self.main_page.locators.HIDDEN_TCPDUMP_EXAMPLES_BUTTON)
        with allure.step('Clicked to Tcpdump button in popup menu'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url
        self.driver.switch_to.window(self.driver.window_handles[1])
        with allure.step('Switched to next tab'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert 'Tcpdump Examples' in self.driver.title


class TestMainPageBodyButtons(UIBaseCase):

    def test_click_to_api_picture(self):
        """
           This test checks "API" round icon in main page body.

           Starting page:
               Main page

           Test steps:
               1. Clicking to "API" button in main page body
               2. Moving to nex tab
               3. Asserting "API" in tab title

           Expected result:
               Opened new tab with "API" in tab title
        """

        self.main_page.find_elements_list(self.main_page.locators.BODY_PICTURES)[0].click()
        with allure.step('Clicked to API picture in main page body'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url
        self.driver.switch_to.window(self.driver.window_handles[1])
        with allure.step('Switched to next tab'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert 'API' in self.driver.title

    def test_click_to_internet_future_picture(self):
        """
           This test checks "Future of the Internet" round icon in main page body.

           Starting page:
               Main page

           Test steps:
               1. Clicking to "Future of the Internet" icon in main page body
               2. Moving to nex tab
               3. Asserting "Future of the Internet" in tab title

           Expected result:
               Opened new tab with "Future of the Internet" in tab title
        """

        self.main_page.find_elements_list(self.main_page.locators.BODY_PICTURES)[1].click()
        with allure.step('Clicked to Internet picture in main page body'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url
        self.driver.switch_to.window(self.driver.window_handles[1])
        with allure.step('Switched to next tab'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert 'Future of the Internet' in self.driver.title

    def test_click_to_smtp_picture(self):
        """
           This test checks "SMTP" round icon in main page body.

           Starting page:
               Main page

           Test steps:
               1. Clicking to "SMTP" icon in main page body
               2. Moving to nex tab
               3. Asserting "SMTP" in tab title

           Expected result:
               Opened new tab with "SMTP" in tab title
        """
        self.main_page.find_elements_list(self.main_page.locators.BODY_PICTURES)[2].click()
        with allure.step('Clicked to Internet picture in main page body'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert self.driver.current_url == self.main_page.url
        self.driver.switch_to.window(self.driver.window_handles[1])
        with allure.step('Switched to next tab'):
            allure.attach(self.driver.get_screenshot_as_png(), 'Page statue', allure.attachment_type.PNG)
        assert 'SMTP' in self.driver.title
