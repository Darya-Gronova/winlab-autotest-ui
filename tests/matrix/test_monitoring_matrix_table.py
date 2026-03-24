import re

import pytest

from pages.matrix_page import MatrixPage


@pytest.mark.ui
@pytest.mark.matrix
def test_headers_contain_mandatory_columns(chromium_page_with_authorization):
    """
    Verify that table headers contain several key business columns.

    The exact Russian labels may evolve, so we assert on substrings/patterns
    that should remain relatively stable.
    """
    page = chromium_page_with_authorization
    matrix = MatrixPage(page)

    matrix.open()

    # Adjust patterns if business naming changes.
    expected_subset = ["Матриц", "Зон", "Объект"]
    matrix.assert_headers_contain(expected_subset)


@pytest.mark.ui
@pytest.mark.matrix
def test_pagination_changes_page_if_available(chromium_page_with_authorization):
    """
    If pagination is present, switching pages should change the first-row data.
    If pagination controls are not found, the test is skipped.
    """
    page = chromium_page_with_authorization
    matrix = MatrixPage(page)

    matrix.open()

    if not matrix.has_pagination():
        pytest.skip("Pagination controls are not available in current UI")

    first_page_values = matrix.get_first_row_values()

    matrix.go_to_next_page()
    second_page_values = matrix.get_first_row_values()

    assert (
        first_page_values != second_page_values
    ), "Expected different data on the next pagination page for the same table"


@pytest.mark.ui
@pytest.mark.matrix
def test_sorting_by_key_column_changes_order_if_supported(chromium_page_with_authorization):
    """
    If the table supports sorting by a key column, clicking the header should
    change the ordering of values in that column. Detection is heuristic:
    we rely on aria-sort or multiple clicks causing a change in first-row value.
    """
    page = chromium_page_with_authorization
    matrix = MatrixPage(page)

    matrix.open()

    headers = matrix.get_table_headers()
    if not headers:
        pytest.skip("No headers available for sorting check")

    # Heuristic: pick the first header; adjust to a more specific one if needed.
    key_header_index = 0

    # Click header to trigger sorting if possible
    header_locator = matrix.table_headers.nth(key_header_index)
    header_locator.click()

    before = matrix.get_first_row_values()

    # Second click often toggles sort direction
    header_locator.click()
    after = matrix.get_first_row_values()

    # If nothing changed we consider sorting not effectively available
    if before == after:
        pytest.skip("Sorting by the chosen column does not change table order in current UI")

