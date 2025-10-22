import pytest
from playwright.sync_api import expect, Page


def test_successful_authorization(chromium_page: Page):  # Создаем тестовую функцию

    # Переходим на страницу входа
    chromium_page.goto("https://devatlaskm.marketing-logic.ru/authorization")

    # Заполняем поле логин
    login_input = page.get_by_test_id('login-input').locator('input')
    login_input.fill("apetrovikh")

    # Проверяем, что в поле находится ожидаемое значение
    expect( login_input).to_have_value("apetrovikh")

    # Заполняем поле пароль
    password_input = chromium_page.locator('//*[@id="root"]/div/div/div/div/div/input[2]')
    password_input.fill("2S9u7m2d5s")

    # Проверяем, что в поле находится ожидаемое значение
    expect(password_input).to_have_value("2S9u7m2d5s")

    # Нажимаем на кнопку Login
    login_button = chromium_page.locator('//*[@id="root"]/div/div/div/div/div/button')
    login_button.click()

    # Проверяем авторизацию по меню
    navigation = chromium_page.locator('//*[@id="root"]/div/div/div/header/div[2]/div[1]/ul')

    # Проверяем, что каждый текст есть внутри блока
    expect(navigation).to_contain_text("Мониторинг")
    expect(navigation).to_contain_text("Объекты")
    expect(navigation).to_contain_text("Справочники")
