import pytest
from api.api_base import *
from database.db_base import *
import allure


class TestLoginApi(NonAuthorizedApiBase, MySqlBase):

    def test_getting_app_status_with_no_authorize(self):
        """
            This test checks application status from API.

            Session:
                Non-authorized

            Test steps:
                1. Sending http request to check application status
                2. Asserting response status code

            Expected result:
                Response status code equals to 200
        """

        response_status_code = self.api_client.get_app_status()
        assert response_status_code == 200

    def test_login_user(self):
        """
            This test checks login from API.

            Session:
                Non-authorized

            Test steps:
                1. Sending http request to log in registered user  ( method: POST )
                2. Asserting response status code
                3. Sending sql query to get required row
                4. Asserting "active=1" in sql response

            Expected result:
                Response status code equals to 302 and user has attribute active == 1 in database
        """

        response_status_code = self.api_client.post_login()
        assert response_status_code == 302
        db_req = str(self.get_table(username=self.api_client.username))
        assert 'active=1' in db_req


class TestPositiveApi(AuthorizedApiBase, MySqlBase):

    @allure.severity('Major')
    def test_register_user(self, random_user_data):  # BUG
        """
            This test checks register user from API.

            Session:
                Authorized

            Test steps:
                1. Sending http request to register user  ( method: POST )
                2. Sending sql query to get required row
                3. Asserting that row has not NULL values

            Expected result:
                Row has not NULL values
        """

        self.api_client.post_register_user(info=random_user_data)
        db_req = str(self.get_table(username=random_user_data['username'])).split('start_active_time')[0]
        assert 'None' not in db_req

    @allure.severity('Minor')
    def test_add_user(self, random_user_data):  # BUG
        """
            This test checks user adding API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to add user ( method: POST )
                2. Asserting response status code
                3. Sending sql query to get required row
                4. Asserting query is not empty

            Expected result:
                Response status code equals to 201 and user added to database
        """

        response_status_code = self.api_client.post_add_user(random_user_data)
        assert response_status_code == 201
        db_req = str(self.get_table(username=random_user_data['username']))
        assert db_req

    @allure.severity('Minor')
    def test_add_user_without_middlename(self, random_user_data):  # BUG
        """
            This test checks user adding API handle.
            Request body has not middle name value

            Session:
                Authorized

            Test steps:
                1. Sending http request to add user  ( method: POST )
                2. Asserting response status code
                3. Sending sql query to get required row
                4. Asserting query is not empty

            Expected result:
                Response status code equals to 201 and user added to database
        """

        random_user_data['middle_name'] = ''
        response_status_code = self.api_client.post_add_user(random_user_data)
        assert response_status_code == 201
        db_req = str(self.get_table(username=random_user_data['username']))
        assert db_req

    def test_getting_vk_id(self):
        """
            This test checks getting vk id API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to get user vk id ( method: GET )
                2. Asserting response status code

            Expected result:
                Response status code equals to 200
        """

        response_status_code = self.api_client.get_vk_id(self.api_client.username)
        assert response_status_code == 200

    def test_deleting_user(self, random_user_data):
        """
            This test checks user deleting API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to register user  ( method: POST )
                2. Sending http request to delete user  ( method: DELETE )
                3. Asserting response status code
                4. Sending sql query to get required row
                5. Asserting query is empty

            Expected result:
                Response status code equals to 204 or 200 and user is not presented in database
        """

        self.api_client.post_register_user(info=random_user_data)
        response_status_code = self.api_client.delete_user(random_user_data['username'])
        assert response_status_code == 204 or response_status_code == 200
        db_req = self.get_table(username=random_user_data['username'])
        assert not db_req

    def test_ban_user(self, random_user_data):
        """
            This test checks user blocking API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to register user  ( method: POST )
                2. Sending http request to block user registered in step 1  ( method: POST )
                3. Asserting response status code
                4. Sending sql query to get required row
                5. Asserting response row has attribute access = 0

            Expected result:
                Response status code equals to 200 and row has attribute access = 0 in database
        """

        self.api_client.post_register_user(info=random_user_data)
        response_status_code = self.api_client.post_block_user(random_user_data['username'])
        assert response_status_code == 200
        db_response = str(self.get_table(username=random_user_data['username']))
        assert 'access=0' in db_response

    def test_unban_user(self, random_user_data):
        """
            This test checks user unblocking API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to register user  ( method: POST )
                2. Sending http request to block user registered in step 1  ( method: POST )
                3. Sending http request to unblock user registered in step 1 ( method: POST )
                4. Asserting response status code
                5. Sending sql query to get required row
                6. Asserting response row has attribute access = 1

            Expected result:
                Response status code equals to 200 and row has attribute access = 1 in database
        """

        username = random_user_data['username']
        self.api_client.post_register_user(info=random_user_data)
        self.api_client.post_block_user(username)
        response_status_code = self.api_client.post_unblock_user(username)
        assert response_status_code == 200
        db_response = str(self.get_table(username=random_user_data['username']))
        assert 'access=1' in db_response

    def test_getting_app_status_with_authorize(self):
        """
            This test checks application status API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to get application status  ( method: GET )
                2. Asserting response status code

            Expected result:
                Response status code equals to 200
        """

        response_status_code = self.api_client.get_app_status()
        assert response_status_code == 200

    @allure.severity('Critical')
    def test_changing_password(self, random_user_data):  # BUG
        """
            This test checks changing user password API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to register user  ( method: POST )
                2. Sending http request to change user password registered in step 1  ( method: PUT )
                3. Asserting response status code
                4. Sending sql query to get required row
                5. Asserting password has been changed

            Expected result:
                Response status code equals to 200 and row has attribute password = new password in database
        """

        new_password = '12345678'
        self.api_client.post_register_user(info=random_user_data)
        response_status_code = self.api_client.put_change_user_password(username=random_user_data['username'],
                                                                        password=new_password)
        assert response_status_code == 200
        db_req = str(self.get_table(username=random_user_data['username']))
        assert f'password={new_password}' in db_req


class TestNegativeNonAuthorizedApi(NonAuthorizedApiBase, MySqlBase):

    def test_negative_authorizing_non_existing_user(self, random_user_data):
        """
            This negative test checks non-existing user login API handle.

            Session:
                Non-authorized

            Test steps:
                1. Sending http request to log in non-existing user  ( method: POST )
                2. Asserting response status code
                3. Sending sql query to get required row
                4. Asserting queried row is empty

            Expected result:
                Response status code equals to 401 and queried row is empty
        """

        response_status_code = self.api_client.post_login(info=random_user_data)
        assert response_status_code == 401
        db_resp = self.get_table(username=random_user_data['username'])
        assert not db_resp

    def test_negative_deleting_non_authorized_session(self, random_user_data):
        """
            This negative test checks deleting user API handle.
            Session is not authorized

            Session:
                Non-authorized

            Test steps:
                1. Sending http request to register user ( method: POST )
                2. Sending http request to delete user ( method: DELETE )
                2. Asserting response status code
                3. Sending sql query to get required row
                4. Asserting queried row is not empty

            Expected result:
                Response status code equals to 401 and queried row is not empty
        """

        self.api_client.post_register_user(info=random_user_data)
        response_status_code = self.api_client.delete_user(random_user_data['username'])
        assert response_status_code == 401
        db_resp = self.get_table(username=random_user_data['username'])
        assert db_resp

    def test_negative_add_user_non_authorized_session(self, random_user_data):
        """
            This negative test checks adding user API handle.
            Session is not authorized

            Session:
                Non-authorized

            Test steps:
                1. Sending http request to add user ( method: POST )
                2. Asserting response status code
                3. Sending sql query to get required row
                4. Asserting queried row is empty

            Expected result:
                Response status code equals to 401 and queried row is empty
        """

        response_status_code = self.api_client.post_add_user(random_user_data)
        assert response_status_code == 401
        db_req = self.get_table(username=random_user_data['username'])
        assert not db_req

    def test_negative_block_user_non_authorized_session(self):
        """
            This negative test checks blocking user API handle.
            Session is not authorized

            Session:
                Non-authorized

            Test steps:
                1. Sending http request to block existing user ( method: POST )
                2. Asserting response status code
                3. Sending sql query to get required row
                4. Asserting queried row has attribute active = 1

            Expected result:
                Response status code equals to 401 and queried row has attribute active = 1
        """

        response_status_code = self.api_client.post_block_user(self.api_client.username)
        assert response_status_code == 401
        db_req = str(self.get_table(username=self.api_client.username))
        assert 'active=1' in db_req

    def test_negative_unblock_user_non_authorized_session(self):
        """
            This negative test checks unblocking user API handle.
            Session is not authorized

            Session:
                Non-authorized

            Test steps:
                1. Sending http request to unblock existing user ( method: POST )
                2. Asserting response status code
                3. Sending sql query to get required row
                4. Asserting queried row has attribute active = 1

            Expected result:
                Response status code equals to 401 and queried row has attribute active = 1
        """

        response_status_code = self.api_client.post_unblock_user(self.api_client.username)
        assert response_status_code == 401
        db_req = str(self.get_table(username=self.api_client.username))
        assert 'active=1' in db_req

    def test_negative_changing_password_non_authorized_session(self):
        """
            This negative test checks changing user password API handle.
            Session is not authorized

            Session:
                Non-authorized

            Test steps:
                1. Sending http request to change existing user password ( method: PUT )
                2. Asserting response status code
                3. Sending sql query to get required row
                4. Asserting password did not change in database

            Expected result:
                Response status code equals to 401 and password did not change in database
        """
        new_password = '12345678'
        response_status_code = self.api_client.put_change_user_password(username=self.api_client.username,
                                                                        password=new_password)
        assert response_status_code == 401
        db_req = str(self.get_table(username=self.api_client.username))
        assert f'password={self.api_client.password}' in db_req


class TestNegativeAuthorizedApi(AuthorizedApiBase, MySqlBase):

    def test_authorizing_non_existing_user(self, random_user_data):
        """
            This negative test checks authorizing non-existing user API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to log in non-existing user ( method: POST )
                2. Asserting response status code
                3. Sending sql query to get required row
                4. Asserting queried row is empty

            Expected result:
                Response status code equals to 401 and user is not presented in database
        """

        response_status_code = self.api_client.post_login(info=random_user_data)
        assert response_status_code == 401
        db_resp = self.get_table(username=random_user_data['username'])
        assert not db_resp

    def test_deleting_non_existing_user(self, random_user_data):
        """
            This negative test checks deleting non-existing user API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to delete non-existing user ( method: DELETE )
                2. Asserting response status code
                3. Sending sql query to get required row
                4. Asserting queried row is empty

            Expected result:
                Response status code equals to 404 and user is not presented in database
        """

        response_status_code = self.api_client.delete_user(random_user_data['username'])
        assert response_status_code == 404
        db_resp = self.get_table(username=random_user_data['username'])
        assert not db_resp

    def test_block_non_existing_user(self, random_user_data):
        """
            This negative test checks block non-existing user API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to block non-existing user ( method: POST )
                2. Asserting response status code

            Expected result:
                Response status code equals to 404
        """

        response_status_code = self.api_client.post_block_user(random_user_data['username'])
        assert response_status_code == 404

    def test_unblock_non_existing_user(self, random_user_data):
        """
            This negative test checks unblock non-existing user API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to unblock non-existing user ( method: POST )
                2. Asserting response status code

            Expected result:
                Response status code equals to 404
        """

        response_status_code = self.api_client.post_unblock_user(random_user_data['username'])
        assert response_status_code == 404

    def test_changing_password_non_existing_user(self, random_user_data):
        """
            This negative test checks changing password to non-existing user API handle.

            Session:
                Authorized

            Test steps:
                1. Sending http request to change password to non-existing user ( method: PUT )
                2. Asserting response status code

            Expected result:
                Response status code equals to 404
        """

        new_password = '12345678'
        response_status_code = self.api_client.put_change_user_password(random_user_data['username'],
                                                                        new_password)
        assert response_status_code == 404


class TestNegativeIncorrectRequests(AuthorizedApiBase, MySqlBase):

    @allure.severity('Major')
    def test_changing_password_incorrect_request(self, random_user_data):  # BUG
        """
            This negative test checks changing user password API handle.
            Old and new passwords are the same.

            Session:
                Authorized

            Test steps:
                1. Sending http request to register user ( method: POST )
                2. Sending http request to log in user registered in step 1 ( method: POST )
                3. Sending http request to change user password registered in step 1 ( method: PUT )
                4. Asserting response status code
                5. Sending sql query to get required row
                6. Asserting queried row has attribute with the same password

            Expected result:
                Response status code equals to 400 and password did not change in database
        """

        self.api_client.post_register_user(info=random_user_data)
        self.api_client.post_login(info=random_user_data)
        response_status_code = self.api_client.put_change_user_password(random_user_data['username'],
                                                                        random_user_data['password'])
        assert response_status_code == 400
        db_req = str(self.get_table(username=random_user_data['username']))
        assert random_user_data['password'] in db_req

    @allure.severity('Major')
    @pytest.mark.parametrize('field', ['first_name', 'username', 'last_name', 'password', 'email'])  # everything BUG
    def test_add_user_with_empty_field_authorized(self, random_user_data, field):
        """
             This negative test checks adding user API handle with one empty field in request.

             Session:
                 Authorized

             Test steps:
                 1. Sending http request to add user with empty field ( method: POST )
                 2. Asserting response status code
                 3. Sending sql query to get required row
                 4. Asserting queried row is empty

             Expected result:
                 Response status code equals to 400 and user was not created in database
        """

        random_user_data[field] = ''
        response_status_code = self.api_client.post_add_user(random_user_data)
        assert response_status_code == 400
        db_req = self.get_table(username=random_user_data['username'])
        assert not db_req

    @allure.severity('Major')
    @pytest.mark.parametrize('field', ['first_name', 'username', 'last_name', 'password', 'email'])  # everything BUG
    def test_add_user_null_fields_authorized(self, random_user_data, field):
        """
             This negative test checks adding user API handle with one None field in request.

             Session:
                 Authorized

             Test steps:
                 1. Sending http request to add user with None field ( method: POST )
                 2. Asserting response status code
                 3. Sending sql query to get required row
                 4. Asserting queried row is empty

             Expected result:
                 Response status code equals to 400 and user was not created in database
        """

        random_user_data[field] = None
        response_status_code = self.api_client.post_add_user(random_user_data)
        assert response_status_code == 400
        db_req = self.get_table(username=random_user_data['username'])
        assert not db_req


class TestNegativeIncorrectRequestsNonAuthorized(NonAuthorizedApiBase, MySqlBase):

    @allure.severity('Minor')
    @pytest.mark.parametrize('field', ['username', 'password'])
    def test_authorizing_incorrect_request(self, random_user_data, field):  # EVERYTHING BUG
        """
             This negative test checks authorizing user API handle with one empty field in request.

             Session:
                 Non-authorized

             Test steps:
                 1. Sending http request to register user ( method: POST )
                 2. Sending http request to add user with empty field ( method: POST )
                 3. Asserting response status code
                 4. Sending sql query to get required row
                 5. Asserting queried row has attribute active = 0

             Expected result:
                 Response status code equals to 401 and user is not authorized according to the database
        """

        self.api_client.post_register_user(info=random_user_data)
        random_user_data[field] = None
        response_status_code = self.api_client.post_login(info=random_user_data, redirects=True)
        assert response_status_code == 401
        db_req = str(self.get_table(username=random_user_data['username']))
        assert 'active=0' in db_req

    @pytest.mark.parametrize('field', ['first_name', 'username', 'last_name', 'password', 'email'])
    def test_add_user_incorrect_request_non_authorized_session(self, random_user_data, field):
        """
             This negative test checks adding user from API with None field in request.

             Session:
                 Non-authorized

             Test steps:
                 1. Sending http request to add user with empty field ( method: POST )
                 2. Asserting response status code
                 3. Sending sql query to get required row
                 4. Asserting queried row is empty

             Expected result:
                 Response status code equals to 401 and user is not presented in database
        """

        random_user_data[field] = None
        response_status_code = self.api_client.post_add_user(random_user_data)
        assert response_status_code == 401
        if field == 'username':
            db_req = self.get_table(email=random_user_data['email'])
        else:
            db_req = self.get_table(username=random_user_data['username'])
        assert not db_req


class TestNegativeDoubleRequests(AuthorizedApiBase, MySqlBase):
    def test_double_add_user(self, random_user_data):
        """
             This negative test checks double adding user from API.

             Session:
                 Authorized

             Test steps:
                 1. Sending http request to add user ( method: POST )
                 2. Sending http request to add same user ( method: POST )
                 3. Asserting response status code
                 4. Sending sql query to get required row
                 5. Asserting queried row is correct

             Expected result:
                 Response status code equals to 304 or 400 and user is presented in database
        """

        self.api_client.post_add_user(random_user_data)
        response_status_code = self.api_client.post_add_user(random_user_data)
        assert response_status_code == 304 or response_status_code == 400
        db_req = str(self.get_table(username=random_user_data['username']))
        assert random_user_data['username'] in db_req

    @allure.severity('Minor')
    def test_double_register_user(self, random_user_data):  # BUG
        """
             This negative test checks register user from API.

             Session:
                 Authorized

             Test steps:
                 1. Sending http request to register user ( method: POST )
                 2. Sending http request to register same user ( method: POST )
                 3. Asserting response status code
                 4. Sending sql query to get required row
                 5. Asserting queried row is correct

             Expected result:
                 Response status code equals to 400 or 304 and user is presented in database
        """

        self.api_client.post_register_user(info=random_user_data)
        response_status_code = self.api_client.post_register_user(info=random_user_data)
        assert response_status_code == 304 or response_status_code == 400
        db_req = str(self.get_table(username=random_user_data['username']))
        assert random_user_data['username'] in db_req
