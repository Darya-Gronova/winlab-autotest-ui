import pytest
from pages.matrix_page import MatrixPage
from pages.menu_page import MenuPage
from playwright.sync_api import expect


@pytest.mark.matrix
def test_open_monitoring_matrix_authorized(chromium_page_with_authorization):
    """Open monitoring matrix page using saved `browser-state.json` and check main elements."""
    page = chromium_page_with_authorization
    matrix = MatrixPage(page=page)
    menu = MenuPage(page=page)

    matrix.visit('https://devatlaskm.marketing-logic.ru/monitoring/matrix')

    # Check navbar/menu is visible (indicates authorized view)
    menu.check_menu_link()

    # Check main matrix-specific elements
    expect(matrix.tab_monitoring_matrix_link).to_be_visible()
    expect(matrix.filter_matrix).to_be_visible()
    expect(matrix.tree_zone_expand_button).to_be_visible()
