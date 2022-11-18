from selenium.webdriver.common.by import By


class BasePageLocators:
    LOGIN_BUTTON = (By.XPATH, '//*[contains(@class,"responseHead-module-button")]')
    LOGIN_FIELD = (By.XPATH, '//*[@name="email"]')
    PASSWORD_FIELD = (By.XPATH, '//*[@name="password"]')
    AUTHORIZATION_BUTTON = (By.XPATH, '//*[contains(@class,"authForm-module-button")]')


class MainPageLocators(BasePageLocators):
    PERSON_MODULE = (By.XPATH, '//*[contains(@class,"right-module-rightButton") and'
                               ' contains(@class,"right-module-mail")]')

    CREATE_CAMPAIGN_BUTTON = (By.XPATH, '//*[contains(@class,"button-module-button") and'
                                        ' contains(@class,"button-module-blue") and'
                                        ' contains(@class,"button-module-button")]')
    CREATE_CAMPAIGN_BUTTON_PRIMARY = (By.XPATH, '//*[@href="/campaign/new"]')
    TABLE_CONTROLS_MODULE = (By.XPATH, '//*[contains(@class,"tableControls-module-controlsWrap")]')

    AUDIENCES_MODULE = (By.XPATH, '//*[@href="/segments"]')
    CREATE_AUDIENCE_BUTTON = (By.XPATH, '//*[@class="button button_submit"]')
    CREATE_AUDIENCE_BUTTON_PRIMARY = (By.XPATH, '//*[@href="/segments/segments_list/new/"]')

    COMPANY_SEARCH_INPUT = (By.XPATH, '//input[@type="text"]')
    SELECT_ALL_BUTTON = (By.XPATH, '//*[contains(@class,"optionListTitle-module-controls")]')
    ELEMENTS_CAMPAIGNS_LIST = (By.XPATH, '//*[contains(@class,"nameCell-module-campaignNameLink")]')


class CreateCampaignPageLocators(BasePageLocators):
    CONVERSION_TRAFFIC_BUTTON = (By.XPATH, '//*[@cid="view694"]')
    CREATE_CAMPAIGN_BUTTON = (By.XPATH, '//*[@cid="view642"]')
    SAVE_IMAGE_BUTTON = (By.XPATH, '//*[@class="image-cropper__save js-save"]')

    AD_LINK_INPUT = (By.XPATH, '//*[@data-gtm-id="ad_url_text"]')
    AD_TITLE_INPUT = (By.XPATH, '//*[@data-name="title_25"]')
    AD_BODY_INPUT = (By.XPATH, '//*[@data-name="text_90"]')
    AD_FORMAT_MULTIFORMAT = (By.XPATH, '//*[@cid="view811"]')

    CAMPAIGN_NAME_INPUT = (By.XPATH, '//*[@class="input__inp js-form-element" and @maxlength="255"]')

    BODY_UPLOAD_BUTTON = (By.XPATH, '//*[@data-test="image_1080x607"]')
    ICON_UPLOAD_BUTTON = (By.XPATH, '//*[@data-test="icon_256x256"]')

    CAMPAIGNS_LIST_TABLE = (By.XPATH, '//*[contains(@class,"label-module-labelWrapper")]')


class CreateSegmentPageLocators(BasePageLocators):
    AUDIENCE_SEGMENT_LIST = (By.XPATH, '//*[@data-class-name="TypeItemView"]')
    CHECKBOX_LIST = (By.XPATH, '//*[@class="adding-segments-source__checkbox js-main-source-checkbox"]')

    ADD_SEGMENT_BUTTON = (By.XPATH, '//*[@class="adding-segments-modal__btn-wrap js-add-button"]')
    SEGMENT_NAME_INPUT = (By.XPATH, '//*[@class="input__inp js-form-element" and @maxlength="60"]')
    CREATE_SEGMENT_BUTTON = (By.XPATH, '//*[@class="button button_submit"]')

    GROUP_DATA_SOURCE = (By.XPATH, '//*[@href="/segments/groups_list"]')
    GROUP_LINK_INPUT = (By.XPATH, '//*[contains(@class,"multiSelectSuggester-module-searchInput") and'
                                  ' contains(@class,"input-module-input") and'
                                  ' contains(@class,"input-module-input")]')

    SELECT_ALL_BUTTON = (By.XPATH, '//*[contains(@class,"optionListTitle-module-control") and @data-test="select_all"]')
    ADD_SELECTED_BUTTON = (By.XPATH, '//*[contains(@class,"button-module-textWrapper")]')

    SEGMENTS_LIST_TABLE = (By.XPATH, '//*[@data-id="dragHandler"]')
    VK_OK_GROUPS_DATA_TABLE = (By.XPATH, '//*[@class="flexi-table__header flexi-table__column-width '
                                         'js-flexi-table-header"]')

    DELETE_GROUP_BUTTON = (By.XPATH, '//*[@data-class-name="RemoveView"]')
    CONFIRM_DELETE_GROUP_BUTTON = (By.XPATH, '//*[@class="button button_confirm-remove button_general"]')

    SEGMENT_SEARCH_INPUT = (By.XPATH, '//input[@type="text"]')
    POPUP_SELECTED = (By.XPATH, '//*[contains(@class,"suggester-module-option") and'
                                ' contains(@class,"optionsList-module-option")]')

    SEGMENTS_LIST = (By.XPATH, '//*[contains(@href,"/segments/segments_list/")]')
    SEGMENT_INTERACTIVE_BUTTON = (By.XPATH, '//*[@type="checkbox"]')
    ACTIONS_BUTTON = (By.XPATH, '//*[contains(@class,"select-module-selectWrap") and'
                                ' contains(@class,"segmentsTable-module-controlItem")]')
    REMOVE_BUTTON = (By.XPATH, '//*[contains(@class,"optionsList-module-option") and'
                               ' contains(@class,"optionsList-module-hasScroll")]')
