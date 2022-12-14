from selenium.webdriver.common.by import By


class LoginPageLocators:
    REGISTER_BUTTON = (By.XPATH, '//a[@href="/reg"]')
    LOGIN_BUTTON = (By.XPATH, '//input[@id="submit"]')
    USERNAME_FIELD = (By.XPATH, '//input[@id="username"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@id="password"]')

    HIDDEN_ALERT_FIELD = (By.XPATH, '//*[@id="flash"]')


class RegisterPageLocators:
    LOGIN_BUTTON = (By.XPATH, '//a[@href="/login"]')
    REGISTER_BUTTON = (By.XPATH, '//input[@id="submit"]')
    NAME_FIELD = (By.XPATH, '//input[@id="user_name"]')
    SURNAME_FIELD = (By.XPATH, '//input[@id="user_surname"]')
    MIDDLENAME_FIELD = (By.XPATH, '//input[@id="user_middle_name"]')
    USERNAME_FIELD = (By.XPATH, '//input[@id="username"]')
    EMAIL_FIELD = (By.XPATH, '//input[@id="email"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@id="password"]')
    PASSWORD_FIELD_CONFIRM = (By.XPATH, '//input[@id="confirm"]')
    CHECKBOX_BUTTON = (By.XPATH, '//input[@id="term"]')

    HIDDEN_ALERT_FIELD = (By.XPATH, '//*[@id="flash"]')


class MainPageLocators:
    LOGOUT_BUTTON = (By.XPATH, '//a[@href="/logout"]')

    APP_BUTTON = (By.XPATH, '//a[@class="uk-navbar-brand uk-hidden-small"]')
    HOME_BUTTON = (By.XPATH, '//a[@href="/"]')
    HEADER_BUTTONS = (By.XPATH, '//li[contains(@class, "uk-parent")]')

    HIDDEN_PYTHON_LINK = (By.XPATH, '//div[@class="uk-dropdown uk-dropdown-navbar uk-dropdown-bottom" and'
                                    '      @aria-hidden="false"]/ul/li[1]')
    HIDDEN_FLASK_LINK = (By.XPATH, '//div[@class="uk-dropdown uk-dropdown-navbar uk-dropdown-bottom" and'
                                   '      @aria-hidden="false"]/ul/li[2]')
    HIDDEN_CENTOS_LINK = (By.XPATH, '//div[@class="uk-dropdown uk-dropdown-navbar uk-dropdown-bottom" and'
                                    '      @aria-hidden="false"]/ul/li[1]')

    HIDDEN_WIRESHARK_NEWS_BUTTON = (By.XPATH, '//ul[@class="uk-nav uk-nav-navbar"]/li[1]/ul[@class="uk-nav-sub"]/li[1]/a')
    HIDDEN_WIRESHARK_DOWNLOAD_BUTTON = (By.XPATH, '//ul[@class="uk-nav uk-nav-navbar"]/li[1]/ul['
                                                  '     @class="uk-nav-sub"]/li[2]/a')
    HIDDEN_TCPDUMP_EXAMPLES_BUTTON = (By.XPATH, '//ul[@class="uk-nav uk-nav-navbar"]/li[2]/ul/li[1]')

    USERNAME_STRING = (By.XPATH, '//div[@id="login-name"]/ul/li[1]')
    VK_ID_STRING = (By.XPATH, '//div[@id="login-name"]/ul/li[3]')

    BODY_PICTURES = (By.XPATH, '//*[@class="uk-overlay uk-overlay-hover"]')

    HINT_FIELD = (By.XPATH, '//*[@class="uk-text-center uk-text-large"]/p')
