import pytest
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from playwright.sync_api import expect


@pytest.mark.authorization
def test_login_page_elements(login_page: LoginPage):
    """Проверяет наличие полей логина/пароля и кнопки авторизации"""
    login_page.visit('https://devatlaskm.marketing-logic.ru/authorization')
    expect(login_page.login_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.login_button).to_be_visible()


@pytest.mark.authorization
def test_successful_login(login_page: LoginPage, menu_page: MenuPage):
    """Тест успешной авторизации с корректными учётными данными"""
    login_page.visit('https://devatlaskm.marketing-logic.ru/authorization')
    # Рабочие креды
    login_page.fill_login_form(login='dariak', password='r63l80AV')
    login_page.click_login_button()
    menu_page.check_menu_link()


@pytest.mark.authorization
@pytest.mark.parametrize('login,password', [
    ('wrong', 'wrong'),
    ('dariak', 'wrongpass'),
    ('', ''),
])
def test_invalid_or_empty_credentials(login_page: LoginPage, login: str, password: str):
    """Проверяет поведение при некорректных или пустых данных"""
    login_page.visit('https://devatlaskm.marketing-logic.ru/authorization')
    login_page.fill_login_form(login=login, password=password)
    login_page.click_login_button()
    login_page.check_visible_wrong_login_or_password_alert()
