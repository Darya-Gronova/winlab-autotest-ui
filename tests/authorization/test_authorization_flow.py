import os
from pathlib import Path

import pytest
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from playwright.sync_api import expect

from pages.login_page import AUTH_URL


AUTH_LOGIN = os.environ.get("AUTH_LOGIN", "dariak")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD", "r63l80AV")
SAVE_STATE_FLAG_VALUES = ("1", "true", "True")


@pytest.mark.authorization
def test_login_page_elements(login_page: LoginPage):
    """Проверяет наличие полей логина/пароля и кнопки авторизации"""
    login_page.open()
    expect(login_page.login_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.login_button).to_be_visible()


@pytest.mark.authorization
def test_successful_login(login_page: LoginPage, menu_page: MenuPage):
    """
    Тест успешной авторизации с корректными учётными данными.

    При выставленной переменной окружения SAVE_BROWSER_STATE_ON_SUCCESS=1
    дополнительно сохраняет storage_state в browser-state.json, который затем
    используется фикстурой chromium_page_with_authorization.
    """
    login_page.open()

    # Рабочие креды берём из окружения с разумным fallback.
    login_page.login(login=AUTH_LOGIN, password=AUTH_PASSWORD)

    # Дополнительная проверка через MenuPage для сохранения семантики
    # существующих тестов.
    menu_page.check_menu_link()

    if os.environ.get("SAVE_BROWSER_STATE_ON_SUCCESS", "0") in SAVE_STATE_FLAG_VALUES:
        state_path = Path("browser-state.json")
        login_page.page.context.storage_state(path=str(state_path))


@pytest.mark.authorization
@pytest.mark.parametrize(
    "login,password",
    [
        ("invalid_user", "invalid_password"),
        ("", ""),
    ],
)
def test_invalid_or_empty_credentials(login_page: LoginPage, login: str, password: str):
    """Проверяет поведение при некорректных или пустых данных"""
    login_page.open()
    login_page.fill_login_form(login=login, password=password)
    login_page.click_login_button()
    login_page.check_visible_wrong_login_or_password_alert()
