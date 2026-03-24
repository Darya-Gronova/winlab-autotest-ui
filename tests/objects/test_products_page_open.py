import pytest
from pages.products_page import ProductsPage
from playwright.sync_api import Page


@pytest.mark.ui
@pytest.mark.objects
@pytest.mark.smoke
def test_open_products_page_authorized(chromium_page_with_authorization: Page) -> None:
    """
    Smoke: authorized user can open /objects/products and see basic layout.
    """
    page = ProductsPage(chromium_page_with_authorization)
    page.open()
    page.assert_basic_layout_loaded()

