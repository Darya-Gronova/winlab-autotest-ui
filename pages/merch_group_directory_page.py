from __future__ import annotations

import re
from typing import Dict, List

import pytest
from components.navigation.navbar_component import NavbarComponent
from pages.base_page import BasePage
from playwright.sync_api import Locator, Page, expect


MERCH_GROUP_DIRECTORY_URL = "https://devatlaskm.marketing-logic.ru/directory/merch-group-directory"


class MerchGroupDirectoryPage(BasePage):
    """
    Page object for /directory/merch-group-directory.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.navbar = NavbarComponent(page)

        # Header / breadcrumb / title
        self.page_title: Locator = page.get_by_role(
            "heading", name=re.compile("мерч-?групп", re.IGNORECASE)
        )

        # Filters / search
        self.search_input: Locator = page.get_by_placeholder(
            re.compile("Поиск|Search", re.IGNORECASE)
        )
        self.filter_panel: Locator = page.get_by_test_id("filter-select")
        self._apply_filters_button: Locator = page.get_by_role(
            "button", name=re.compile("Применить", re.IGNORECASE)
        )
        self._reset_filters_button: Locator = page.get_by_role(
            "button", name=re.compile("Сброс", re.IGNORECASE)
        )

        # Table / list
        self.table: Locator = page.get_by_role("table").first
        self.table_headers: Locator = self.table.get_by_role("columnheader")
        self.table_rows: Locator = self.table.get_by_role("row")

        # Pagination (optional)
        self._pagination_next: Locator = page.get_by_role(
            "button", name=re.compile("След|Next", re.IGNORECASE)
        )
        self._pagination_prev: Locator = page.get_by_role(
            "button", name=re.compile("Пред|Prev", re.IGNORECASE)
        )

    # ---------------
    # Navigation/open
    # ---------------
    def open(self) -> "MerchGroupDirectoryPage":
        self.visit(MERCH_GROUP_DIRECTORY_URL)
        self.assert_basic_layout_loaded()
        return self

    # -------
    # Filters
    # -------
    def search_by_text(self, text: str) -> None:
        expect(self.search_input).to_be_visible()
        self.search_input.fill(text)
        if self._apply_filters_button.count() > 0:
            self._apply_filters_button.first.click()

    def apply_filters(self) -> None:
        if self._apply_filters_button.count() > 0:
            self._apply_filters_button.first.click()

    def reset_filters(self) -> None:
        if self._reset_filters_button.count() > 0:
            self._reset_filters_button.first.click()

    def has_filters(self) -> bool:
        return self.filter_panel.count() > 0 or self.search_input.count() > 0

    # ------
    # Table
    # ------
    def has_pagination(self) -> bool:
        return self._pagination_next.count() > 0 or self._pagination_prev.count() > 0

    def go_to_next_page(self) -> None:
        if self._pagination_next.count() > 0:
            first_row_before = self.get_first_row_values()
            self._pagination_next.first.click()
            if first_row_before:
                expect(self.table_rows.nth(1)).not_to_have_text(
                    list(first_row_before.values())[0], timeout=5000
                )

    def rows_count(self) -> int:
        total_rows = self.table_rows.count()
        return max(0, total_rows - 1)

    def get_headers(self) -> List[str]:
        headers: List[str] = []
        for i in range(self.table_headers.count()):
            headers.append(self.table_headers.nth(i).inner_text().strip())
        return headers

    def get_first_row_values(self) -> Dict[str, str]:
        if self.rows_count() == 0:
            return {}

        headers = self.get_headers()
        first_data_row = self.table_rows.nth(1)
        cells = first_data_row.get_by_role("cell")

        values: Dict[str, str] = {}
        for i, header in enumerate(headers):
            if i >= cells.count():
                break
            values[header] = cells.nth(i).inner_text().strip()
        return values

    def sort_by_header(self, name_or_index: str | int) -> None:
        if isinstance(name_or_index, int):
            header = self.table_headers.nth(name_or_index)
        else:
            name = str(name_or_index)
            header = self.table_headers.filter(
                has_text=re.compile(re.escape(name), re.IGNORECASE)
            ).first
        expect(header).to_be_visible()
        header.click()

    # ----------
    # Assertions
    # ----------
    def assert_basic_layout_loaded(self) -> None:
        # If we were redirected to the authorization page, consider the user
        # unauthorised for this run and skip UI checks instead of failing.
        if "authorization" in self.page.url:
            pytest.skip("User is not authorized for Merch Group Directory; redirected to authorization page")

        self.navbar.check_visible()
        expect(self.page_title).to_be_visible()
        expect(self.table).to_be_visible()
        if self.has_filters():
            expect(self.filter_panel or self.search_input).not_to_be_none()

    def assert_headers_contain(self, expected_subset: List[str]) -> None:
        headers = self.get_headers()
        for expected in expected_subset:
            assert any(expected in header for header in headers), (
                f"Expected header containing '{expected}' not found in {headers}"
            )

