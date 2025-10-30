from playwright.sync_api import sync_playwright, expect


def test_successful_authorization():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Переходим на страницу входа
        page.goto("https://devatlaskm.marketing-logic.ru/authorization")

        # Заполняем поле логин
        login_input = page.get_by_test_id('login-input')
        login_input.fill("dariak")

        # Проверяем, что в поле находится ожидаемое значение
        expect(login_input).to_have_value("dariak")

        # Заполняем поле пароль
        password_input = page.get_by_test_id('password-input')
        password_input.fill("r63l80AV")

        # Проверяем, что в поле находится ожидаемое значение
        expect(password_input).to_have_value("r63l80AV")

        # Нажимаем на кнопку Login
        login_button = page.get_by_test_id('login-button')
        login_button.click()

        context.storage_state(path="browser-state.json")

        # Проверяем авторизацию по меню
        navigation = page.locator('//*[@id="root"]/div/div/div/header/div[2]/div[1]/ul')

        # Проверяем, что каждый текст есть внутри блока
        expect(navigation).to_contain_text("Мониторинг")
        expect(navigation).to_contain_text("Объекты")
        expect(navigation).to_contain_text("Справочники")

def test_failed_authorization():
    with sync_playwright() as p:
        ...