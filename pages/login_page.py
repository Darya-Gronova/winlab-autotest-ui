from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.login_input = page.get_by_test_id('login-input')
        self.password_input = page.get_by_test_id('password-input')
        self.login_button = page.get_by_test_id('login-button')
        self.wrong_login_or_password_alert = page.locator('//*[@id="root"]/div/div/div/div/div/p')

    def fill_login_form(self, login: str, password: str):
        self.login_input.fill(login)
        expect(self.login_input).to_have_value(login)

        self.password_input.fill(password)
        expect(self.password_input).to_have_value(password)

    def click_login_button(self):
        self.login_button.click()

    def check_visible_wrong_login_or_password_alert(self):
        expect(self.wrong_login_or_password_alert).to_be_visible()
        expect(self.wrong_login_or_password_alert).to_have_text('Неверный логин или пароль')