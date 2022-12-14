from ui.pages.base_page import BasePage
from ui.locators import basic_locators


class MainPage(BasePage):

    locators = basic_locators.MainPageLocators()
    url = 'http://app:8080/welcome/'

