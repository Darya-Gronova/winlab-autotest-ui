import pytest
from pages.products_page import ProductsPage
from playwright.sync_api import Page


@pytest.mark.ui
@pytest.mark.objects
def test_products_text_search_changes_first_row_when_possible(
    chromium_page_with_authorization: Page,
) -> None:
    """
    Применение простого текстового поиска должно менять первую строку таблицы
    (если данные позволяют).
    """
    page = ProductsPage(chromium_page_with_authorization).open()

    if not page.has_filters():
        pytest.skip("Products page has no visible filters/search controls")

    first_row_before = page.get_first_row_values()

    # Вводим часть названия или кода, не завязываясь на конкретные значения.
    page.search_by_text("1")
    first_row_after = page.get_first_row_values()

    if not first_row_before or not first_row_after:
        pytest.skip("Not enough data rows to assert filter effect")

    assert first_row_before != first_row_after, "Expected first row to change after applying text search filter"


@pytest.mark.ui
@pytest.mark.objects
def test_products_reset_filters_restores_table_state_when_possible(
    chromium_page_with_authorization: Page,
) -> None:
    """
    Сброс фильтров должен возвращать таблицу в исходное состояние
    (при наличии явной кнопки сброса).
    """
    page = ProductsPage(chromium_page_with_authorization).open()

    if not page.has_filters():
        pytest.skip("Products page has no visible filters/search controls")

    first_row_initial = page.get_first_row_values()
    page.search_by_text("1")

    if not hasattr(page, "reset_filters"):
        pytest.skip("No explicit reset_filters implementation on ProductsPage")

    page.reset_filters()
    first_row_after_reset = page.get_first_row_values()

    if not first_row_initial or not first_row_after_reset:
        pytest.skip("Not enough data rows to assert reset effect")

    assert (
        first_row_initial == first_row_after_reset
    ), "Expected table state after reset to match the initial state"

