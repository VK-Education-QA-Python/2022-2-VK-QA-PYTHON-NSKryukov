from ui.pages.base_page import BasePageANDROID
from ui.locators.locators_android import ApplicationPageANDROIDLocators
import allure
import os
from ui.capability import capability_select


class ApplicationPageANDROID(BasePageANDROID):
    locators = ApplicationPageANDROIDLocators()

    @allure.step('Checking application version')
    def check_version(self):
        application_version = self.find(self.locators.APPLICATION_VERSION).text
        apk_version = os.path.basename(capability_select()['app']).replace('apk', '_').split('_')[1][:-1]
        return apk_version in application_version

    @allure.step('Checking application trademark')
    def check_trademark(self):
        application_trademark = self.find(self.locators.APPLICATION_TRADEMARK).text
        return 'Все права защищены' in application_trademark
