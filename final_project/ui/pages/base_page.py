from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import allure


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 10
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.element_to_be_clickable(locator))

    def find_without_waiting(self, locator):
        return self.driver.find_element(*locator)

    def find_element_wait_until_presence(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_elements_list(self, locator, timeout=None):
        self.wait(timeout).until(EC.element_to_be_clickable(locator))
        return self.driver.find_elements(*locator)

    def click_to_element(self, locator):
        return self.find(locator).click()

    def put_in_element(self, locator, info):
        element = self.find(locator)
        element.clear()
        element.send_keys(info)

    def move_to_element(self, locator):
        element = self.find(locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()
        with allure.step('Moving cursor to element'):
            allure.attach(self.get_png_screenshot(), 'Statue', allure.attachment_type.PNG)

    def get_png_screenshot(self):
        return self.driver.get_screenshot_as_png()
