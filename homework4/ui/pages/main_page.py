from ui.pages.base_page import BasePageANDROID
from ui.locators.locators_android import MainPageANDROIDLocators
import allure


class MainPageANDROID(BasePageANDROID):
    locators = MainPageANDROIDLocators()

    @allure.step('Skipping preview')
    def skip_preview(self):
        self.click(self.locators.SKIP_PREVIEW)

    @allure.step('Going to settings menu')
    def go_to_settings_menu(self):
        self.click(self.locators.BURGER_MENU)

    @allure.step('Writing command')
    def enter_command(self, command_text: str):
        self.click(self.locators.KEYBOARD_BUTTON, timeout=10)
        self.send_keys(self.locators.COMMAND_LINE_INPUT, command_text)
        self.click(self.locators.SEND_TEXT_BUTTON, timeout=10)

    @allure.step('Swiping and click to required field')
    def swipe_and_click_to_population_button(self):
        self.swipe_left_to_element_in_line(self.locators.POPULATION_FIELD, self.locators.LINE_ELEMENTS,
                                           self.locators.SUGGESTS_LIST, 5)
        self.click(self.locators.POPULATION_FIELD)

    @allure.step('Checking answer')
    def check_answer(self, locator, answer):
        answer_element = self.find_elements(locator)[1]
        return answer_element.text == f'{answer}'
