from ui.locators import basic_locators
from ui.pages.base_page import BasePage
import allure


class MainPage(BasePage):
    locators = basic_locators.MainPageLocators()
    url = 'https://target-sandbox.my.com/dashboard'

    @allure.step('Going to creating company page')
    def go_to_create_campaign_page(self):
        self.find(self.locators.CREATE_CAMPAIGN_BUTTON, timeout=30).click()

    @allure.step('Going to creating segment page')
    def go_to_create_segment_page(self):
        self.find(self.locators.AUDIENCES_MODULE, timeout=30).click()
        self.find(self.locators.CREATE_AUDIENCE_BUTTON).click()

    @allure.step('Going to audiences page')
    def go_to_audiences_page(self):
        self.find(self.locators.AUDIENCES_MODULE, timeout=30).click()

    def entity_is_added(self, entity_name):
        return self.existing_of_entity(entity_name)

    @allure.step('Deleting required segment')
    def delete_segment(self, tag, segment_name):
        segment_index = self.find_element_index_in_table(self.locators.SEGMENTS_LIST, tag, segment_name)
        self.find_elements_list(self.locators.DELETE_AUDIENCE_BUTTONS)[segment_index].click()
        self.find(self.locators.ACTIONS_BUTTON).click()
        self.find(self.locators.REMOVE_BUTTON).click()
        with allure.step('Taking screenshot: segments list while deleting required segment'):
            allure.attach(self.get_png_screenshot(), 'list_state_while_deleting_required_segment',
                          allure.attachment_type.PNG)
