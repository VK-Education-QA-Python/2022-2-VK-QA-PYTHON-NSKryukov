from selenium.webdriver.common.by import By

LOGIN_BUTTON = (By.XPATH, '//*[contains(@class,"responseHead-module-button")]')
LOGIN_FIELD = (By.XPATH, '//*[@name="email"]')
PASSWORD_FIELD = (By.XPATH, '//*[@name="password"]')
AUTHORIZATION_BUTTON = (By.XPATH, '//*[contains(@class,"authForm-module-button")]')

PERSON_MODULE = (By.XPATH, '//*[contains(@class,"right-module-rightButton") and'
                           ' contains(@class,"right-module-mail")]')
FAILED_AUTH_FIELD = (By.XPATH, '//*[contains(@class,"notify-module-content") and'
                               ' contains(@class,"undefined notify-module-error") and'
                               ' contains(@class,"notify-module-notifyBlock")]')

POPUP_BUTTONS = (By.XPATH, '//*[contains(@class,"rightMenu-module-rightMenuLink")]')

PAGE_CHECK = (By.XPATH, '//*[contains(@class,"instruction-module-title")]')

PROFILE_BUTTON = (By.XPATH, '//*[contains(@class,"center-module-button") and'
                            ' contains(@class, "center-module-profile")]')
BILLING_BUTTON = (By.XPATH, '//*[contains(@class,"center-module-button") and'
                            ' contains(@class, "center-module-billing")]')
PROFILE_CHECK = (By.XPATH, '//*[@class = "left-nav__group__label"]')
BILLING_CHECK = (By.XPATH, '//*[@class = "page-tabs__tab-item js-tab-item"]')

CONTACT_INFORMATION_FIELDS = (By.XPATH, '//*[@class = "input__inp js-form-element"]')
SAVE_BUTTON = (By.XPATH, '//*[@class = "button__text"]')
SUCCESS_NOTIFICATION = (By.XPATH, '//*[@class = "_notification__content js-notification-content"]')
