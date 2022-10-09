import pytest
from src import basic_locators
from base import BaseCase
from src.authorization_data import *
from src.profile_data import *


@pytest.mark.UI
class TestTask(BaseCase):
    def test_authorization_positive(self):
        self.authorization(POSITIVE_EMAIL, POSITIVE_PASSWORD)
        assert self.find(*basic_locators.PERSON_MODULE), 'Authorization failed'

    def test_logout(self):
        self.authorization(POSITIVE_EMAIL, POSITIVE_PASSWORD)
        self.logout()
        assert self.find(*basic_locators.LOGIN_BUTTON)

    def test_authorization_negative_first(self):
        self.authorization(NEGATIVE_EMAIL_FIRST, NEGATIVE_PASSWORD_FIRST)
        assert self.find(*basic_locators.FAILED_AUTH_FIELD)

    def test_authorization_negative_second(self):
        self.authorization(NEGATIVE_EMAIL_SECOND, NEGATIVE_PASSWORD_SECOND)
        assert self.find(*basic_locators.FAILED_AUTH_FIELD)

    def test_profile_setting(self):
        self.authorization(POSITIVE_EMAIL, POSITIVE_PASSWORD)
        self.change_profile_data(CONTACT_INFORMATION)
        assert self.find(*basic_locators.SUCCESS_NOTIFICATION).is_displayed()

    @pytest.mark.parametrize('locator, verification',
                             [(basic_locators.PROFILE_BUTTON, basic_locators.PROFILE_CHECK),
                              (basic_locators.BILLING_BUTTON, basic_locators.BILLING_CHECK)])
    def test_center_module_buttons(self, locator, verification):
        self.authorization(POSITIVE_EMAIL, POSITIVE_PASSWORD)
        self.find(*locator).click()
        assert self.find(*verification)
