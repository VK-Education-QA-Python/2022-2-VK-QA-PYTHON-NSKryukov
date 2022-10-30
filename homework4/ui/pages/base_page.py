import logging
from ui.locators.locators_android import BasePageANDROIDLocators
import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction


logger = logging.getLogger('test')


class BasePageANDROID(object):
    locators = BasePageANDROIDLocators()

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

        logger.info(f'{self.__class__.__name__} page is opening...')

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        self.find(locator)
        return self.driver.find_elements(*locator)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def click(self, locator, timeout=None):
        element = self.find(locator, timeout)
        element.click()

    def send_keys(self, locator, text):
        element = self.find(locator)
        element.send_keys(text)

    def swipe_up(self, swipetime=200):
        action = TouchAction(self.driver)
        dimension = self.driver.get_window_size()
        x = int(dimension['width'] / 2)
        start_y = int(dimension['height'] * 0.6)
        end_y = int(dimension['height'] * 0.2)
        action. \
            press(x=x, y=start_y). \
            wait(ms=swipetime). \
            move_to(x=x, y=end_y). \
            release(). \
            perform()

    def swipe_down(self, swipetime=200):
        dimension = self.driver.get_window_size()
        x = int(dimension['width'] / 2)
        start_y = int(dimension['height'] * 0.2)
        end_y = int(dimension['height'] * 0.6)
        action = TouchAction(self.driver)
        action. \
            press(x=x, y=start_y). \
            wait(ms=swipetime). \
            move_to(x=x, y=end_y). \
            release(). \
            perform()

    def swipe_up_to_element(self, locator, max_swipes):
        already_swiped = 0
        while len(self.driver.find_elements(*locator)) == 0:
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")
            self.swipe_up()
            already_swiped += 1

    def swipe_down_to_element(self, locator, max_swipes):
        already_swiped = 0
        while len(self.driver.find_elements(*locator)) == 0:
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")
            self.swipe_down()
            already_swiped += 1

    def swipe_left_to_element_in_line(self, locator, element_locator, line_locator, max_swipes):
        already_swiped = 0
        while len(self.driver.find_elements(*locator)) == 0:
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")

            self.swipe_element_lo_left(element_locator, line_locator)
            already_swiped += 1

    def swipe_element_lo_left(self, element_locator, line_locator):
        web_element = self.find_elements(element_locator)[-1]
        web_line = self.find(line_locator, 5)
        web_element_left_x = web_element.location['x']
        web_element_upper_y = web_element.location['y']
        web_element_lower_y = web_element_upper_y + web_element.rect['height']
        web_element_middle_y = (web_element_upper_y + web_element_lower_y) / 2
        web_line_left_x = web_line.location['x']
        action = TouchAction(self.driver)
        action. \
            press(x=web_element_left_x, y=web_element_middle_y). \
            wait(ms=300). \
            move_to(x=web_line_left_x, y=web_element_middle_y). \
            release(). \
            perform()
