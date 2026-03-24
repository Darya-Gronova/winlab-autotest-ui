import pytest

from pages.matrix_page import MatrixPage


@pytest.mark.ui
@pytest.mark.matrix
def test_filter_matrix_by_first_option_changes_table(chromium_page_with_authorization):
    """
    Apply the first available filter option and verify that table data changes.
    The assertion is based on structural change (first-row values) rather than
    specific static dataset.
    """
    page = chromium_page_with_authorization
    matrix = MatrixPage(page)

    matrix.open()
    before = matrix.get_first_row_values()

    # Use index-based selection to avoid hard-coding concrete option texts.
    matrix.select_matrix_filter_by_index(0)
    matrix.apply_filters()

    after = matrix.get_first_row_values()
    assert before != after, "Expected table data to change after applying filter"


@pytest.mark.ui
@pytest.mark.matrix
def test_reset_filters_restores_default_state(chromium_page_with_authorization):
    """
    After applying a filter, resetting filters should restore the default table state.
    """
    page = chromium_page_with_authorization
    matrix = MatrixPage(page)

    matrix.open()
    baseline = matrix.get_first_row_values()

    matrix.select_matrix_filter_by_index(0)
    matrix.apply_filters()
    filtered = matrix.get_first_row_values()
    assert baseline != filtered, "Precondition: filter should change table data"

    matrix.reset_filters()
    restored = matrix.get_first_row_values()
    assert (
        restored == baseline
    ), "Expected table data to return to its default state after resetting filters"


@pytest.mark.ui
@pytest.mark.matrix
def test_multiple_filters_combination_if_available(chromium_page_with_authorization):
    """
    If there are multiple filters, combining them should lead to a narrower or at
    least different result set. If only a single filter exists, test is skipped.
    """
    page = chromium_page_with_authorization
    matrix = MatrixPage(page)

    matrix.open()

    if not matrix.has_multiple_filters():
        pytest.skip("Multiple filters are not available in current UI")

    baseline_rows = matrix.rows_count()

    # Apply first two filters (indices 0 and 1 as a generic approach)
    matrix.select_matrix_filter_by_index(0)
    matrix.select_matrix_filter_by_index(1)
    matrix.apply_filters()

    combined_rows = matrix.rows_count()

    assert combined_rows <= baseline_rows or combined_rows == 0

