import os
import requests
import allure


class ApiClient:

    def __init__(self):
        self.username = None
        self.password = None
        self.session = requests.Session()

    def post_register_user(self, repo_root=None, info=None):

        url = 'http://localhost:8082/reg'
        if repo_root:
            with open(os.path.join(repo_root, 'source', 'default_user_data_api.txt'), 'r') as f:
                info_array = f.readline().split(' ')

            self.username = info_array[3]
            self.password = info_array[5]
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
        else:
            data = {
                'name': info['first_name'],
                'surname': info['last_name'],
                'middlename': info['middle_name'],
                'username': info['username'],
                'email': info['email'],
                'password': info['password'],
                'confirm': info['password'],
                'term': 'y',
                'submit': 'Register'
            }
        with allure.step('Sending http requests to register user'):
            allure.attach(f'method: POST, url: {url}, body: {data}', 'request_info', allure.attachment_type.TEXT)
        response = requests.post(url=url, data=data, allow_redirects=True)
        with allure.step('Getting request'):
            allure.attach(f'status_code: {response.status_code}, content: {response.text}',
                          'response_info', allure.attachment_type.TEXT)
        return response.status_code

    def post_login(self, info=None, redirects=False):

        url = 'http://localhost:8082/login'
        if info:
            data = {
                'username': info['username'],
                'password': info['password']
            }
        else:
            data = {
                'username': self.username,
                'password': self.password,
            }
        with allure.step('Sending http requests to login'):
            allure.attach(f'method: POST, url: {url}, body: {data}', 'request_info', allure.attachment_type.TEXT)
        response = self.session.post(url=url, data=data, allow_redirects=redirects)
        with allure.step('Getting request'):
            allure.attach(f'status_code: {response.status_code}, content: {response.text}',
                          'response_info', allure.attachment_type.TEXT)
        return response.status_code

    def post_add_user(self, info):

        url = 'http://localhost:8082/api/user'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'name': info['first_name'],
            'surname': info['last_name'],
            'username': info['username'],
            'password': info['password'],
            'email': info['email'],
        }

        if middle_name := info['middle_name']:
            data['middle_name'] = middle_name
        with allure.step('Sending http requests to add new user'):
            allure.attach(f'method: POST, url: {url}, headers: {headers}, body: {data}',
                          'request_info', allure.attachment_type.TEXT)
        response = self.session.post(url=url, json=data, headers=headers)
        with allure.step('Getting request'):
            allure.attach(f'status_code: {response.status_code}, content: {response.text}',
                          'response_info', allure.attachment_type.TEXT)
        return response.status_code

    def delete_user(self, username):

        url = f'http://localhost:8082/api/user/{username}'
        with allure.step('Sending http requests to delete user'):
            allure.attach(f'method: DELETE, url: {url}', 'request_info', allure.attachment_type.TEXT)
        response = self.session.delete(url=url)
        with allure.step('Getting request'):
            allure.attach(f'status_code: {response.status_code}, content: {response.text}',
                          'response_info', allure.attachment_type.TEXT)
        return response.status_code

    def get_vk_id(self, username):

        url = f'http://localhost:8083/vk_id/{username}'
        with allure.step('Sending http requests to get user vk id'):
            allure.attach(f'method: GET, url: {url}', 'request_info', allure.attachment_type.TEXT)
        response = self.session.get(url=url)
        with allure.step('Getting request'):
            allure.attach(f'status_code: {response.status_code}, content: {response.text}',
                          'response_info', allure.attachment_type.TEXT)
        return response.status_code

    def put_change_user_password(self, username, password):

        url = f'http://localhost:8082/api/user/{username}/change-password'
        data = {
            "password": password
        }
        with allure.step('Sending http requests to change user password'):
            allure.attach(f'method: PUT, url: {url}', 'request_info', allure.attachment_type.TEXT)
        response = self.session.put(url=url, data=data)
        with allure.step('Getting request'):
            allure.attach(f'status_code: {response.status_code}, content: {response.text}',
                          'response_info', allure.attachment_type.TEXT)
        return response.status_code

    def post_block_user(self, username):

        url = f'http://localhost:8082/api/user/{username}/block'
        with allure.step('Sending http requests to block user'):
            allure.attach(f'method: PUT, url: {url}', 'request_info', allure.attachment_type.TEXT)
        response = self.session.post(url=url)
        with allure.step('Getting request'):
            allure.attach(f'status_code: {response.status_code}, content: {response.text}',
                          'response_info', allure.attachment_type.TEXT)
        return response.status_code

    def post_unblock_user(self, username):

        url = f'http://localhost:8082/api/user/{username}/accept'
        with allure.step('Sending http requests to unblock user'):
            allure.attach(f'method: POST, url: {url}', 'request_info', allure.attachment_type.TEXT)
        response = self.session.post(url=url)
        with allure.step('Getting request'):
            allure.attach(f'status_code: {response.status_code}, content: {response.text}',
                          'response_info', allure.attachment_type.TEXT)
        return response.status_code

    def get_app_status(self):

        url = 'http://localhost:8082/status'
        with allure.step('Sending http requests to get app status'):
            allure.attach(f'method: GET, url: {url}', 'request_info', allure.attachment_type.TEXT)
        response = self.session.get(url=url)
        with allure.step('Getting request'):
            allure.attach(f'status_code: {response.status_code}, content: {response.text}',
                          'response_info', allure.attachment_type.TEXT)
        return response.status_code
