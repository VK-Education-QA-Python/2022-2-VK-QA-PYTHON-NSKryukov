from ui.locators import basic_locators
from ui.pages.base_page import BasePage
import allure


class CreateCampaignPage(BasePage):
    locators = basic_locators.CreateCampaignPageLocators()
    url = 'https://target-sandbox.my.com/campaign/new'

    @allure.step('Creating campaign with objective - Traffic')
    def create_campaign(self, *args, locators=locators, file_path, name=None):
        self.find(locators.CONVERSION_TRAFFIC_BUTTON).click()
        self.find(locators.AD_LINK_INPUT).send_keys(args[0])
        self.scroll_until_visible(locators.CAMPAIGN_NAME_INPUT)
        self.put_in_element(locators.CAMPAIGN_NAME_INPUT, name)
        self.scroll_until_visible(locators.AD_FORMAT_MULTIFORMAT)
        self.find(locators.AD_FORMAT_MULTIFORMAT).click()
        self.scroll_until_visible(locators.AD_TITLE_INPUT)
        self.put_in_element(locators.AD_TITLE_INPUT, args[1])
        self.put_in_element(locators.AD_BODY_INPUT, args[2])
        self.upload_in_hidden_input(locators.ICON_UPLOAD_BUTTON, file_path)
        self.find(locators.SAVE_IMAGE_BUTTON).click()
        self.upload_in_hidden_input(locators.BODY_UPLOAD_BUTTON, file_path)
        self.find(locators.SAVE_IMAGE_BUTTON).click()
        self.find(locators.CREATE_CAMPAIGN_BUTTON).click()
        self.find(locators.CAMPAIGNS_LIST_TABLE, timeout=30)
        with allure.step('Taking screenshot: campaigns list after creating new campaign'):
            allure.attach(self.get_png_screenshot(), 'list_state_after_adding_new_campaign',
                          allure.attachment_type.PNG)
