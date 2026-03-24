import pytest
from pages.matrix_page import MatrixPage


@pytest.mark.ui
@pytest.mark.matrix
@pytest.mark.smoke
def test_open_monitoring_matrix_authorized(chromium_page_with_authorization):
    """
    Smoke: open Monitoring Matrix page using saved `browser-state.json`
    and verify that the basic layout is loaded.
    """
    page = chromium_page_with_authorization
    matrix = MatrixPage(page=page)

    matrix.open()

    # Basic layout (navbar, tabs, filters, tree, table)
    matrix.assert_basic_layout_loaded()

    # By default the Monitoring Matrix tab should be active
    assert matrix.is_tab_active("matrix"), "Expected Monitoring Matrix tab to be active by default"
