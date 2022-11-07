from appium.webdriver.common.mobileby import MobileBy as By


class BasePageANDROIDLocators:
    pass


class MainPageANDROIDLocators(BasePageANDROIDLocators):
    SKIP_PREVIEW = (By.XPATH, '//android.widget.LinearLayout/android.widget.ImageButton')

    KEYBOARD_BUTTON = (By.ID, 'ru.mail.search.electroscope:id/keyboard')
    COMMAND_LINE_INPUT = (By.ID, 'ru.mail.search.electroscope:id/input_text')
    SEND_TEXT_BUTTON = (By.ID, 'ru.mail.search.electroscope:id/text_input_send')
    TEXT_CARD = (By.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_content_text')

    SUGGESTS_LIST = (By.ID, 'ru.mail.search.electroscope:id/suggests_list')
    LINE_ELEMENTS = (By.XPATH, '//android.widget.TextView')
    SURFACE_BUTTON = (By.XPATH, '//android.widget.TextView[contains(@text, "площадь россии")]')
    FACT_TITLE_FIELD = (By.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_title')

    DIALOG_ITEMS = (By.XPATH, '//*[contains(@resource-id, '
                              '"ru.mail.search.electroscope:id/dialog_item")]')

    BURGER_MENU = (By.ID, 'ru.mail.search.electroscope:id/assistant_menu_bottom')

    NEWS_TRACK = (By.ID, 'ru.mail.search.electroscope:id/player_track_name')


class SettingsPageANDROIDLocators(BasePageANDROIDLocators):
    NEWS_SOURCE_BUTTON = (By.ID, 'ru.mail.search.electroscope:id/user_settings_field_news_sources')
    ABOUT_APPLICATION_BUTTON = (By.ID, 'ru.mail.search.electroscope:id/user_settings_about')


class NewsSourcePageANDROIDLocators(BasePageANDROIDLocators):
    MAIL_RU_NEWS_SOURCE = (By.XPATH, '//*[contains(@resource-id, '
                                     '"ru.mail.search.electroscope:id/news_sources_item_title")'
                                     ' and contains(@text, "Mail.Ru")]')
    CONFIRMATION_SIGN = (By.ID, 'ru.mail.search.electroscope:id/news_sources_item_selected')


class ApplicationPageANDROIDLocators(BasePageANDROIDLocators):
    APPLICATION_VERSION = (By.ID, 'ru.mail.search.electroscope:id/about_version')
    APPLICATION_TRADEMARK = (By.ID, 'ru.mail.search.electroscope:id/about_copyright')
