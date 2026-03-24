import pytest
from pages.merch_group_directory_page import MerchGroupDirectoryPage
from playwright.sync_api import Page


@pytest.mark.ui
@pytest.mark.directory
def test_merch_group_directory_text_search_changes_first_row_when_possible(
    chromium_page_with_authorization: Page,
) -> None:
    """
    Применение текстового поиска/фильтра по мерч-группам должно менять первую строку
    (если данные позволяют).
    """
    page = MerchGroupDirectoryPage(chromium_page_with_authorization).open()

    if not page.has_filters():
        pytest.skip("Merch Group Directory page has no visible filters/search controls")

    first_row_before = page.get_first_row_values()
    page.search_by_text("1")
    first_row_after = page.get_first_row_values()

    if not first_row_before or not first_row_after:
        pytest.skip("Not enough data rows to assert filter effect in Merch Group Directory")

    assert (
        first_row_before != first_row_after
    ), "Expected first row to change after applying text search filter in Merch Group Directory"


@pytest.mark.ui
@pytest.mark.directory
def test_merch_group_directory_reset_filters_restores_table_state_when_possible(
    chromium_page_with_authorization: Page,
) -> None:
    """
    Сброс фильтров должен возвращать таблицу в исходное состояние
    (при наличии явной кнопки сброса).
    """
    page = MerchGroupDirectoryPage(chromium_page_with_authorization).open()

    if not page.has_filters():
        pytest.skip("Merch Group Directory page has no visible filters/search controls")

    first_row_initial = page.get_first_row_values()
    page.search_by_text("1")

    if not hasattr(page, "reset_filters"):
        pytest.skip("No explicit reset_filters implementation on MerchGroupDirectoryPage")

    page.reset_filters()
    first_row_after_reset = page.get_first_row_values()

    if not first_row_initial or not first_row_after_reset:
        pytest.skip("Not enough data rows to assert reset effect in Merch Group Directory")

    assert (
        first_row_initial == first_row_after_reset
    ), "Expected table state after reset to match the initial state in Merch Group Directory"

