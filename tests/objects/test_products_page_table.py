import pytest
from pages.products_page import ProductsPage
from playwright.sync_api import Page


@pytest.mark.ui
@pytest.mark.objects
def test_products_table_has_mandatory_columns(chromium_page_with_authorization: Page) -> None:
    """
    Проверяет наличие ключевых колонок в таблице продуктов.
    Проверка по подстрокам, без жёсткого полного списка.
    """
    page = ProductsPage(chromium_page_with_authorization).open()
    page.assert_headers_contain(
        [
            "Код",
            "Наименование",
        ]
    )


@pytest.mark.ui
@pytest.mark.objects
def test_products_pagination_changes_first_row_when_available(
    chromium_page_with_authorization: Page,
) -> None:
    """
    Если на странице есть пагинация, переход на следующую страницу
    должен привести к изменению первой строки (эвристика).
    """
    page = ProductsPage(chromium_page_with_authorization).open()

    if not page.has_pagination():
        pytest.skip("Pagination is not available on Products page")

    first_row_before = page.get_first_row_values()
    page.go_to_next_page()
    first_row_after = page.get_first_row_values()

    # Если данных мало и строка не изменилась — это не ошибка, но логично
    # зафиксировать ожидание изменения.
    assert first_row_before != first_row_after, "Expected first row to change after going to next page"


@pytest.mark.ui
@pytest.mark.objects
def test_products_sorting_by_name_changes_order_when_possible(
    chromium_page_with_authorization: Page,
) -> None:
    """
    Клик по заголовку 'Наименование' (или аналогичному) должен менять порядок строк.
    Если эффекта нет (данные одинаковые), тест может быть флакки и будет помечен как пропуск.
    """
    page = ProductsPage(chromium_page_with_authorization).open()

    headers = page.get_headers()
    if not any("Наимен" in h for h in headers):
        pytest.skip("No suitable 'Name' column found to test sorting")

    first_row_before = page.get_first_row_values()
    page.sort_by_header("Наимен")
    first_row_after = page.get_first_row_values()

    if not first_row_before or not first_row_after:
        pytest.skip("Not enough data rows to assert sorting effect")

    assert first_row_before != first_row_after, "Expected first row to change after sorting by name"

