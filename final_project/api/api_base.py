import pytest


class NonAuthorizedApiBase:
    authorize = False
    register = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, repo_root):
        self.api_client = api_client

        if self.register:
            self.api_client.post_register_user(repo_root=repo_root)
            self.api_client.session.cookies.clear_session_cookies()
        if self.authorize:
            self.api_client.post_login()


class AuthorizedApiBase(NonAuthorizedApiBase):
    authorize = True

