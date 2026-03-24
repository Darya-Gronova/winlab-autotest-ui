import pytest

from pages.matrix_page import MatrixPage


@pytest.mark.ui
@pytest.mark.matrix
def test_tabs_switching_cycle(chromium_page_with_authorization):
    """
    Switch between all monitoring tabs and return to Matrix,
    verifying that the corresponding tab becomes active.
    """
    page = chromium_page_with_authorization
    matrix = MatrixPage(page)

    matrix.open()
    assert matrix.is_tab_active("matrix")

    matrix.go_to_tab_product_classifier()
    assert matrix.is_tab_active("product-classifier")

    matrix.go_to_tab_sales()
    assert matrix.is_tab_active("sales")

    matrix.go_to_tab_realization()
    assert matrix.is_tab_active("realization")

    matrix.go_to_tab_matrix()
    assert matrix.is_tab_active("matrix")

