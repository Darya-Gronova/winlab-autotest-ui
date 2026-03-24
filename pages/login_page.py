import os
import re

from components.navigation.navbar_component import NavbarComponent
from pages.base_page import BasePage
from playwright.sync_api import Locator, Page, expect


AUTH_URL = os.environ.get(
    "AUTH_URL",
    "https://devatlaskm.marketing-logic.ru/authorization",
)


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.login_input: Locator = page.get_by_test_id("login-input")
        self.password_input: Locator = page.get_by_test_id("password-input")
        self.login_button: Locator = page.get_by_test_id("login-button")

        # Error alert after invalid credentials. Prefer a semantic alert role,
        # but fall back to searching by text if needed.
        alert_by_role = page.get_by_role("alert")
        if alert_by_role.count() > 0:
            self.wrong_login_or_password_alert: Locator = alert_by_role.first
        else:
            self.wrong_login_or_password_alert = page.get_by_text(
                re.compile("Неверный логин|Неверный пароль", re.IGNORECASE)
            )

    def open(self) -> "LoginPage":
        """Open the authorization page using a single source of truth URL."""
        self.visit(AUTH_URL)
        return self

    def fill_login_form(self, login: str, password: str):
        self.login_input.fill(login)
        expect(self.login_input).to_have_value(login)

        self.password_input.fill(password)
        expect(self.password_input).to_have_value(password)

    def click_login_button(self):
        self.login_button.click()

    def login(self, login: str, password: str):
        """
        High-level login helper used in tests:
        fill credentials, click login button and wait for main menu.
        """
        self.fill_login_form(login=login, password=password)
        self.click_login_button()

        # After successful authorization, the main navigation bar
        # should become visible. Rely on the shared NavbarComponent
        # to keep behaviour consistent with the rest of the suite.
        navbar = NavbarComponent(self.page)
        navbar.check_menu_link()

    def check_visible_wrong_login_or_password_alert(self):
        expect(self.wrong_login_or_password_alert).to_be_visible()
        expect(self.wrong_login_or_password_alert).to_contain_text("Неверный")