#!/usr/bin/python3
# -*- encoding=utf8 -*-

"""
You can find a basic example of the usage Selenium with PyTest in
 this file.

More info about pytest-selenium:
   https://pytest-selenium.readthedocs.io/en/latest/user_guide.html

How to run:
 1) Download driver for Chrome here:
    https://chromedriver.chromium.org/downloads
 2) Install all requirements:
    pip install -r requirements.txt
 3) Run tests:
    python3 -m pytest -v --driver Chrome --driver-path ~/chrome tests/*
  Remote:
    export SELENIUM_HOST=<moon host>
    export SELENIUM_PORT=4444
    pytest -v --driver Remote --capability browserName chrome tests/*
"""
import pytest

from pages.opensource_demo import MainPage
from config.config import TestData


def test_check_login(web_browser):
    """ Make sure the login page works fine. """

    page = MainPage(web_browser)

    page.username_field.send_keys(TestData.USER_NAME)
    page.password_field.send_keys(TestData.PASSWORD)
    page.login_button.click()

    assert page.dashboard_title.get_text() != TestData.PAGE_TITLE, "Wrong page title"


@pytest.mark.skip(reason="no way of currently testing this")
def test_clicked_links(web_browser):
    """ Test links on the login page work. """

    page = MainPage(web_browser)

    page.linkedin_link.click()
    page.youtube_link.click()
