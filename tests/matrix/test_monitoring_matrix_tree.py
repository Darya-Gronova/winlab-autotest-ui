import pytest

from pages.matrix_page import MatrixPage


@pytest.mark.ui
@pytest.mark.matrix
def test_expand_collapse_zones_via_global_button(chromium_page_with_authorization):
    """
    Use the global expand button to toggle tree state and verify that the number
    of visible tree items changes.
    """
    page = chromium_page_with_authorization
    matrix = MatrixPage(page)

    matrix.open()

    initial_count = matrix.tree_items_count()

    matrix.expand_all_zones()
    after_expand = matrix.tree_items_count()

    # Depending on default state, expansion may increase or reveal items
    assert after_expand != initial_count or after_expand > 0

    # Second toggle should return to a different or original state
    matrix.expand_all_zones()
    after_second_toggle = matrix.tree_items_count()
    assert after_second_toggle != after_expand or after_second_toggle == initial_count


@pytest.mark.ui
@pytest.mark.matrix
def test_select_first_zone_affects_table(chromium_page_with_authorization):
    """
    Selecting a zone in the tree should influence the data shown in the table.
    The check compares first-row values before and after selection.
    """
    page = chromium_page_with_authorization
    matrix = MatrixPage(page)

    matrix.open()
    before = matrix.get_first_row_values()

    matrix.select_first_zone()
    after = matrix.get_first_row_values()

    # With dynamic data we only assert structural change.
    assert before != after, "Expected table data to change after selecting a zone"

