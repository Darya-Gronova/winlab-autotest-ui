import pytest
from playwright.sync_api import expect, Page


def test_matrix(chromium_page: Page):
    # Переходим на страницу входа
    chromium_page.goto("https://devatlaskm.marketing-logic.ru/monitoring/matrix")
