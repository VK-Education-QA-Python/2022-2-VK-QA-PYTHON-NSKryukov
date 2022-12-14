import os
import subprocess
import allure
import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.login_page import LoginPage
from ui.pages.register_page import RegisterPage
from ui.pages.main_page import MainPage
import requests
import faker

faker = faker.Faker()


class RegisterBaseCase:
    driver = None
    authorize = False

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.login_page: LoginPage = (request.getfixturevalue('login_page'))
        self.register_page: RegisterPage = (request.getfixturevalue('register_page'))
        self.main_page: MainPage = (request.getfixturevalue('main_page'))

        if self.authorize:
            cookie = {
                "name": "session",
                "value": request.getfixturevalue('cookies')
            }
            self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.main_page = MainPage(driver)

    @pytest.fixture(scope='function', autouse=True)
    def ui_browser_log(self, driver, repo_root):
        yield
        browser_logs = os.path.join(repo_root, 'browser.log')
        with open(browser_logs, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
        with open(browser_logs, 'r') as f:
            allure.attach(f.read(), 'browser.log', allure.attachment_type.TEXT)

    @pytest.fixture(scope='function', autouse=True)
    def ui_app_log(self, repo_root):
        yield
        app_logs = os.path.join(repo_root, 'app_container.log')
        with open(app_logs, 'w') as f:
            f.write(subprocess.check_output(['docker', 'logs', 'app_container'],
                                            encoding='utf-8', stderr=subprocess.STDOUT))
        with open(app_logs, 'r') as f:
            allure.attach(f.read(), 'app.log', allure.attachment_type.TEXT)

    @pytest.fixture(scope='session', autouse=True)
    def pre_creating_user(self, repo_root):
        with open(os.path.join(repo_root, 'source', 'default_user_data_ui.txt'), 'r') as f:
            info_array = f.readline().split(' ')

        data = {
            'name': info_array[0],
            'surname': info_array[1],
            'middlename': info_array[2],
            'username': info_array[3],
            'email': info_array[4],
            'password': info_array[5],
            'confirm': info_array[5],
            'term': 'y',
            'submit': 'Register'
        }

        requests.post(url='http://localhost:8082/reg', data=data, allow_redirects=True)

        return {'username': data['username'], 'password': data['password']}


class LoginBaseCase(RegisterBaseCase):

    @pytest.fixture(scope='session', autouse=True)
    def pre_creating_users(self):
        data = {
            'name': faker.first_name(),
            'surname': faker.last_name(),
            'middlename': faker.first_name() + 'mid',
            'username': 'testqa',
            'email': faker.email(),
            'password': '123456',
            'confirm': '123456',
            'term': 'y',
            'submit': 'Register'
        }

        requests.post(url='http://localhost:8082/reg', data=data, allow_redirects=True)

        data['username'] = 'testqatestqatest'
        data['email'] = faker.email()
        requests.post(url='http://localhost:8082/reg', data=data, allow_redirects=True)

        data['username'] = 'qatesting'
        data['email'] = faker.email()
        data['password'], data['confirm'] = 'g' * 2
        requests.post(url='http://localhost:8082/reg', data=data, allow_redirects=True)

        data['username'] = 'testingqa'
        data['email'] = faker.email()
        password = '12' * 127 + 'p'
        data['password'], data['confirm'] = password, password
        requests.post(url='http://localhost:8082/reg', data=data, allow_redirects=True)


class UIBaseCase(RegisterBaseCase):
    authorize = True
