import pytest
from pages.merch_group_directory_page import MerchGroupDirectoryPage
from playwright.sync_api import Page


@pytest.mark.ui
@pytest.mark.directory
def test_merch_group_directory_has_mandatory_columns(chromium_page_with_authorization: Page) -> None:
    """
    Проверяет наличие ключевых колонок в таблице мерч-групп
    по подстрокам (без жёсткого полного списка).
    """
    page = MerchGroupDirectoryPage(chromium_page_with_authorization).open()
    page.assert_headers_contain(
        [
            "Код",
            "Наименование",
        ]
    )


@pytest.mark.ui
@pytest.mark.directory
def test_merch_group_directory_pagination_changes_first_row_when_available(
    chromium_page_with_authorization: Page,
) -> None:
    """
    Если на странице есть пагинация, переход на следующую страницу
    должен привести к изменению первой строки (эвристика).
    """
    page = MerchGroupDirectoryPage(chromium_page_with_authorization).open()

    if not page.has_pagination():
        pytest.skip("Pagination is not available on Merch Group Directory page")

    first_row_before = page.get_first_row_values()
    page.go_to_next_page()
    first_row_after = page.get_first_row_values()

    if not first_row_before or not first_row_after:
        pytest.skip("Not enough data rows to assert pagination effect")

    assert (
        first_row_before != first_row_after
    ), "Expected first row to change after going to next page in Merch Group Directory"


@pytest.mark.ui
@pytest.mark.directory
def test_merch_group_directory_sorting_by_name_changes_order_when_possible(
    chromium_page_with_authorization: Page,
) -> None:
    """
    Клик по заголовку 'Наименование' (или аналогичному) должен менять порядок строк.
    Если эффекта нет (данные одинаковые), тест может быть помечен как пропуск.
    """
    page = MerchGroupDirectoryPage(chromium_page_with_authorization).open()

    headers = page.get_headers()
    if not any("Наимен" in h for h in headers):
        pytest.skip("No suitable 'Name' column found to test sorting in Merch Group Directory")

    first_row_before = page.get_first_row_values()
    page.sort_by_header("Наимен")
    first_row_after = page.get_first_row_values()

    if not first_row_before or not first_row_after:
        pytest.skip("Not enough data rows to assert sorting effect in Merch Group Directory")

    assert (
        first_row_before != first_row_after
    ), "Expected first row to change after sorting by name in Merch Group Directory"

