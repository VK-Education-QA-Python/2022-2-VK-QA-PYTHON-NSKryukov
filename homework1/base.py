import pytest
import time
from src import basic_locators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

WAIT_SEC = 7


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def popup_click(self):
        stared_time = time.time()
        while time.time() - stared_time <= 5.0:
            try:
                return self.driver.find_elements(*basic_locators.POPUP_BUTTONS)[1].click()
            except ElementClickInterceptedException:
                time.sleep(0.5)
        raise ElementClickInterceptedException

    def find(self, by, what):
        return self.driver.find_element(by, what)

    def put(self, info, locator):
        search = self.find(*locator)
        search.clear()
        search.send_keys(info)

    @staticmethod
    def put_in_element(element, info):
        element.clear()
        element.send_keys(info)

    def authorization(self, login, password):
        WebDriverWait(self.driver, WAIT_SEC).until(
            EC.element_to_be_clickable(basic_locators.LOGIN_BUTTON))
        self.find(*basic_locators.LOGIN_BUTTON).click()
        self.put(login, basic_locators.LOGIN_FIELD)
        self.put(password, basic_locators.PASSWORD_FIELD)
        self.find(*basic_locators.AUTHORIZATION_BUTTON).click()

    def logout(self):
        WebDriverWait(self.driver, WAIT_SEC).until(
            EC.element_to_be_clickable(basic_locators.PAGE_CHECK))
        self.find(*basic_locators.PERSON_MODULE).click()
        self.popup_click()

    def change_profile_data(self, contact_list):
        self.find(*basic_locators.PROFILE_BUTTON).click()
        input_list = self.driver.find_elements(*basic_locators.CONTACT_INFORMATION_FIELDS)
        for index in range(len(input_list) - 1):
            self.put_in_element(input_list[index], contact_list[index])
        self.find(*basic_locators.SAVE_BUTTON).click()
        WebDriverWait(self.driver, WAIT_SEC).until(EC.visibility_of(self.find(*basic_locators.SUCCESS_NOTIFICATION)))
