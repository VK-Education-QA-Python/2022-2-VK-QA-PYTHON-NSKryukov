import time
from ui.locators import basic_locators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PageNotOpenedException(Exception):
    pass


class BasePage:

    locators = basic_locators.BasePageLocators()
    url = 'https://target-sandbox.my.com/'

    def is_opened(self, timeout=15):
        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url == self.url:
                return True
        raise PageNotOpenedException(f'{self.url} did not open in {timeout} sec, current url {self.driver.current_url}')

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 20
        return WebDriverWait(self.driver, timeout=timeout)

    def login(self, user, password):
        self.find(self.locators.LOGIN_BUTTON).click()
        self.find(self.locators.LOGIN_FIELD).send_keys(user)
        self.find(self.locators.PASSWORD_FIELD).send_keys(password)
        self.find(self.locators.AUTHORIZATION_BUTTON).click()

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.element_to_be_clickable(locator))

    def existing_of_entity(self, name):
        return name in self.driver.page_source

    def find_element_index_in_table(self, table_locator, tag_name, element_name) -> int:
        table = self.driver.find_elements(*table_locator)
        for index in range(len(table) - 1):
            if element_name == table[index].get_attribute(tag_name):
                return index

    def find_elements_list(self, locator, timeout=None):
        self.wait(timeout).until(EC.element_to_be_clickable(locator))
        return self.driver.find_elements(*locator)

    def scroll_until_visible(self, locator):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find(locator))

    def put_in_element(self, locator, info):
        element = self.find(locator)
        element.clear()
        element.send_keys(info)

    def upload(self, locator, file_path):
        self.driver.find(locator).send_keys(file_path)

    def upload_in_hidden_input(self, locator, file_path):
        self.driver.find_element(*locator).send_keys(file_path)

    def get_png_screenshot(self):
        return self.driver.get_screenshot_as_png()

    def set_1920_1080_window_size(self):
        self.driver.set_window_size(1920, 1080)
