import os


def capability_select():
    capability = {"platformName": "Android",
                  "platformVersion": "11.0",
                  "automationName": "Appium",
                  "appPackage": "ru.mail.search.electroscope",
                  "appActivity": "ru.mail.search.electroscope.ui.activity.AssistantActivity",
                  "autoGrantPermissions": "true",
                  "app": os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                      '../marussia_apk/marussia_1.70.0.apk')
                                         ),
                  "orientation": "PORTRAIT"
                  }
    return capability
