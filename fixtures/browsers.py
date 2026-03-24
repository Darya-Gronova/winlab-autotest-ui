import pytest
import os
from playwright.sync_api import Page, Playwright

from pages.login_page import LoginPage


AUTH_LOGIN = os.environ.get("AUTH_LOGIN", "dariak")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD", "r63l80AV")


@pytest.fixture
def chromium_page(playwright: Playwright) -> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()


@pytest.fixture
def chromium_page_with_authorization(playwright: Playwright) -> Page:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(login=AUTH_LOGIN, password=AUTH_PASSWORD)
    yield page
    context.close()
    browser.close()