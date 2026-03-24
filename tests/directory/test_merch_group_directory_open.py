import pytest
from pages.merch_group_directory_page import MerchGroupDirectoryPage
from playwright.sync_api import Page


@pytest.mark.ui
@pytest.mark.directory
@pytest.mark.smoke
def test_open_merch_group_directory_authorized(chromium_page_with_authorization: Page) -> None:
    """
    Smoke: authorized user can open /directory/merch-group-directory and see basic layout.
    """
    page = MerchGroupDirectoryPage(chromium_page_with_authorization)
    page.open()
    page.assert_basic_layout_loaded()

