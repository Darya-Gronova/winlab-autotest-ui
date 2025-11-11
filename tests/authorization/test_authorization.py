import pytest
from pages.login_page import LoginPage

@pytest.mark.authorization
@pytest.mark.parametrize(
    'login, password',
    [
        ('dariak', 'r63l80AV'),
        ('dariak', 'password'),
        ('login', 'r63l80AV')
    ]
)
def test_authorization(chromium_page: LoginPage, login: str, password: str, login_page, menu_page):
    login_page.visit('https://devatlaskm.marketing-logic.ru/authorization')
    login_page.fill_login_form(login=login, password=password)
    login_page.click_login_button()

    try:
        menu_page.check_menu_link()
    except Exception:
        login_page.check_visible_wrong_login_or_password_alert()
