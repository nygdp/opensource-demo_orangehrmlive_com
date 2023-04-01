#!/usr/bin/python3
# -*- encoding=utf8 -*-

import os
from pages.base import WebPage
from pages.elements import WebElement
from config.config import TestData


class MainPage(WebPage):

    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN_URL") or TestData.LOGIN_URL
        super().__init__(web_driver, url)

    # Username field, default Username: Admin
    username_field = WebElement(css_selector="input[placeholder='Username']")

    # Password field, default Password: admin123
    password_field = WebElement(css_selector="input[placeholder='Password']")

    # forgot the password link
    forgot_password_link = WebElement(
        xpath='//p[@class=\'oxd-text oxd-text--p orangehrm-login-forgot-header\']')

    # Submit button
    login_button = WebElement(xpath='//button[@type=\'submit\']')

    # linkedin link
    linkedin_link = WebElement(
        xpath='//a[@href=\'https://www.linkedin.com/company/orangehrm/mycompany/\']//*[name()=\'svg\']')

    # youtube channel link
    youtube_link = WebElement(
        xpath='//a[@href=\'https://www.youtube.com/c/OrangeHRMInc\']//*[name()=\'svg\']')

    # Dashboard page title
    dashboard_title = WebElement(xpath='//*[contains(@title, \'OrangeHRM\')]')
