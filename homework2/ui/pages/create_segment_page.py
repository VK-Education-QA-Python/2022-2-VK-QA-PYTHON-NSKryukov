from ui.locators import basic_locators
from ui.pages.base_page import BasePage
import allure


class CreateSegmentPage(BasePage):
    locators = basic_locators.CreateSegmentPageLocators()
    url = 'https://target-sandbox.my.com/segments/segments_list/new'

    @allure.step('Creating segment from apps and games data-source')
    def create_apps_and_games_segment(self, locators=locators, name=None):
        self.find_elements_list(locators.AUDIENCE_SEGMENT_LIST)[7].click()
        self.find_elements_list(locators.CHECKBOX_LIST)[1].click()
        self.find(locators.ADD_SEGMENT_BUTTON).click()
        self.put_in_element(locators.SEGMENT_NAME_INPUT, name)
        self.find(locators.CREATE_SEGMENT_BUTTON).click()
        self.find(locators.SEGMENTS_LIST_TABLE)
        with allure.step('Taking screenshot: segments list after creating new segment'):
            allure.attach(self.get_png_screenshot(), 'list_state_after_adding_new_segment',
                          allure.attachment_type.PNG)

    @allure.step('Creating "Vk education" group as data-source')
    def create_vk_group_data(self, locators=locators):
        self.find(locators.GROUP_DATA_SOURCE).click()
        self.put_in_element(locators.GROUP_LINK_INPUT, 'https://vk.com/vkedu')
        self.find(locators.SELECT_ALL_BUTTON).click()
        self.find(locators.ADD_SELECTED_BUTTON).click()
        self.find(locators.VK_OK_GROUPS_DATA_TABLE)
        with allure.step('Taking screenshot: state after adding group "Vk education" data-source'):
            allure.attach(self.get_png_screenshot(), 'list_state_after_adding_vk_education_source',
                          allure.attachment_type.PNG)

    @allure.step('Creating segment from vk group data-source')
    def create_vk_group_segment(self, locators=locators, name=None):
        self.find_elements_list(locators.AUDIENCE_SEGMENT_LIST)[9].click()
        self.find_elements_list(locators.CHECKBOX_LIST)[0].click()
        self.find(locators.ADD_SEGMENT_BUTTON).click()
        self.put_in_element(locators.SEGMENT_NAME_INPUT, name)
        self.find(locators.CREATE_SEGMENT_BUTTON).click()
        self.find(locators.SEGMENTS_LIST_TABLE)
        with allure.step('Taking screenshot: segments list after creating "Vk education" group segment'):
            allure.attach(self.get_png_screenshot(), 'list_state_after_adding_vk_group_segment',
                          allure.attachment_type.PNG)

    @allure.step('Deleting "Vk education" group as data-source')
    def delete_vk_group_data(self, locators=locators):
        self.find(locators.GROUP_DATA_SOURCE).click()
        self.set_1920_1080_window_size()
        self.find(locators.DELETE_GROUP_BUTTON).click()
        self.find(locators.CONFIRM_DELETE_GROUP_BUTTON).click()
        with allure.step('Taking screenshot: state while deleting group "Vk education" data-source'):
            allure.attach(self.get_png_screenshot(),
                          'list_state_while_deleting_vk_education_source',
                          allure.attachment_type.PNG)

    @allure.step('Deleting required segment')
    def delete_segment(self, segment_name):
        self.put_in_element(self.locators.SEGMENT_SEARCH_INPUT, segment_name)
        self.find(self.locators.POPUP_SELECTED).click()
        self.find(self.locators.SEGMENT_INTERACTIVE_BUTTON).click()
        self.find(self.locators.ACTIONS_BUTTON).click()
        self.find(self.locators.REMOVE_BUTTON).click()
        with allure.step('Taking screenshot: segments list while deleting required segment'):
            allure.attach(self.get_png_screenshot(), 'list_state_while_deleting_required_segment',
                          allure.attachment_type.PNG)

    def existing_of_segment(self, name):
        self.put_in_element(self.locators.SEGMENT_SEARCH_INPUT, name)
        element = self.find(self.locators.POPUP_SELECTED)
        return element.text == name
