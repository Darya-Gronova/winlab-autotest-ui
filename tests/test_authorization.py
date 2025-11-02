import pytest
from playwright.sync_api import expect

@pytest.mark.authorization
def test_successful_authorization(chromium_page):
        chromium_page.goto("https://devatlaskm.marketing-logic.ru/authorization")

        login_input = chromium_page.get_by_test_id('login-input')
        login_input.fill("dariak")
        expect(login_input).to_have_value("dariak")

        password_input = chromium_page.get_by_test_id('password-input')
        password_input.fill("r63l80AV")

        expect(password_input).to_have_value("r63l80AV")
        login_button = chromium_page.get_by_test_id('login-button')
        login_button.click()

        navigation = chromium_page.get_by_test_id('nav-item-monitoring')
        expect(navigation).to_be_visible()

def test_failed_authorization(chromium_page):

        chromium_page.goto("https://devatlaskm.marketing-logic.ru/authorization")

        login_input = chromium_page.get_by_test_id('login-input')
        login_input.fill("dariak1")

        expect(login_input).to_have_value("dariak1")

        password_input = chromium_page.get_by_test_id('password-input')
        password_input.fill("r63l80AV1")

        expect(password_input).to_have_value("r63l80AV1")

        login_button = chromium_page.get_by_test_id('login-button')
        login_button.click()

        fail_login_and_password = chromium_page.get_by_test_id('fail-login-and-password-input')