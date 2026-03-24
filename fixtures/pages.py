import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.matrix_page import MatrixPage
from pages.menu_page import MenuPage


@pytest.fixture
def login_page(chromium_page: Page) -> LoginPage:
    return LoginPage(page=chromium_page)

@pytest.fixture
def menu_page(chromium_page: Page) -> MenuPage:
    return MenuPage(page=chromium_page)

@pytest.fixture
def matrix_page(chromium_page: Page) -> MatrixPage:
    return MatrixPage(page=chromium_page)