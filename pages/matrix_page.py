from __future__ import annotations

import re
from typing import Dict, List, Pattern

import pytest
from components.navigation.navbar_component import NavbarComponent
from pages.base_page import BasePage
from playwright.sync_api import Locator, Page, expect


MATRIX_URL = "https://devatlaskm.marketing-logic.ru/monitoring/matrix"


class MatrixPage(BasePage):
    """
    Page object for Monitoring Matrix.

    The implementation intentionally relies on:
    - test ids that already exist in the project;
    - generic ARIA roles (table, row, columnheader, treeitem, tab)
      instead of brittle CSS/xpath selectors;
    - soft structural assumptions about filters/tree/table so that tests
      remain as stable as possible with dynamic data.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.navbar = NavbarComponent(page)

        # Tabs
        self.tab_monitoring_matrix_link = page.get_by_test_id("nav-tab-item-monitoring-matrix")
        self.tab_monitoring_product_classifier_link = page.get_by_test_id(
            "nav-tab-item-monitoring-product-classifier"
        )
        self.tab_monitoring_sales_link = page.get_by_test_id("nav-tab-item-monitoring-sales")
        self.tab_monitoring_realization_link = page.get_by_test_id("nav-tab-item-monitoring-realization")

        # Filters
        # The test id already exists; often it represents a container or a list
        # of select controls. We treat it as a collection of filter controls.
        self.filter_matrix: Locator = page.get_by_test_id("filter-select")

        # Optional explicit buttons in the filter panel (identified by text).
        self._apply_filters_button = page.get_by_role("button", name=re.compile("Применить", re.IGNORECASE))
        self._reset_filters_button = page.get_by_role("button", name=re.compile("Сброс", re.IGNORECASE))

        # Tree
        self.tree_zone_expand_button = page.get_by_test_id("expand-button")
        self.tree_items: Locator = page.get_by_role("treeitem")

        # Table / grid
        self.table: Locator = page.get_by_role("table").first
        self.table_headers: Locator = self.table.get_by_role("columnheader")
        self.table_rows: Locator = self.table.get_by_role("row")

        # Pagination (optional, detected in tests)
        self._pagination_next = page.get_by_role("button", name=re.compile("След|Next", re.IGNORECASE))
        self._pagination_prev = page.get_by_role("button", name=re.compile("Пред|Prev", re.IGNORECASE))

    # -----------------
    # Navigation / open
    # -----------------
    def open(self) -> "MatrixPage":
        """
        Navigate to the Monitoring Matrix page and wait for the basic layout.
        """
        self.visit(MATRIX_URL)
        self.assert_basic_layout_loaded()
        return self

    # -------
    # Filters
    # -------
    def filters_count(self) -> int:
        return self.filter_matrix.count()

    def select_matrix_filter_by_index(self, index: int) -> None:
        """
        Select filter option by index.

        The underlying control is addressed through the existing test id.
        """
        expect(self.filter_matrix).to_be_visible()
        self.filter_matrix.nth(index).click()

    def select_matrix_filter_by_text(self, text: str) -> None:
        """
        Select filter option by visible text. The implementation is intentionally
        generic and does not depend on a specific UI library.
        """
        expect(self.filter_matrix).to_be_visible()
        option = self.page.get_by_text(text, exact=False)
        expect(option).to_be_visible()
        option.click()

    def apply_filters(self) -> None:
        """
        Click the 'Apply' button for filters, if it exists.
        """
        if self._apply_filters_button.count() > 0:
            self._apply_filters_button.first.click()

    def reset_filters(self) -> None:
        """
        Click the 'Reset' button for filters, if it exists.
        """
        if self._reset_filters_button.count() > 0:
            self._reset_filters_button.first.click()

    def has_multiple_filters(self) -> bool:
        """
        Helper for tests that want to work with a combination of filters.
        """
        return self.filters_count() > 1

    # -----
    # Tree
    # -----
    def expand_all_zones(self) -> None:
        """
        Toggle expansion for all zones via the global expand button.
        """
        expect(self.tree_zone_expand_button).to_be_visible()
        self.tree_zone_expand_button.click()

    def select_first_zone(self) -> None:
        """
        Select the first available zone in the tree.
        """
        if self.tree_items.count() == 0:
            self.expand_all_zones()
        if self.tree_items.count() > 0:
            self.tree_items.first.click()

    def is_zone_expanded(self, name: str) -> bool:
        """
        Best-effort check using aria-expanded on a treeitem.
        """
        zone = self.page.get_by_role("treeitem", name=re.compile(name, re.IGNORECASE)).first
        if zone.count() == 0:
            return False
        aria_expanded = zone.get_attribute("aria-expanded")
        return aria_expanded == "true"

    def tree_items_count(self) -> int:
        return self.tree_items.count()

    # ------
    # Table
    # ------
    def has_pagination(self) -> bool:
        """
        Best-effort detection of pagination controls.
        """
        return self._pagination_next.count() > 0 or self._pagination_prev.count() > 0

    def go_to_next_page(self) -> None:
        if self._pagination_next.count() > 0:
            self._pagination_next.first.click()

    def go_to_previous_page(self) -> None:
        if self._pagination_prev.count() > 0:
            self._pagination_prev.first.click()

    def rows_count(self) -> int:
        """
        Returns number of data rows (excluding header row).
        """
        total_rows = self.table_rows.count()
        return max(0, total_rows - 1)

    def get_table_headers(self) -> List[str]:
        """
        Return visible text of all table headers.
        """
        headers: List[str] = []
        for i in range(self.table_headers.count()):
            headers.append(self.table_headers.nth(i).inner_text().strip())
        return headers

    def get_first_row_values(self) -> Dict[str, str]:
        """
        Map 'header' -> 'cell value' for the first data row.
        """
        if self.rows_count() == 0:
            return {}

        headers = self.get_table_headers()
        first_data_row = self.table_rows.nth(1)
        cells = first_data_row.get_by_role("cell")

        values: Dict[str, str] = {}
        for i, header in enumerate(headers):
            if i >= cells.count():
                break
            values[header] = cells.nth(i).inner_text().strip()
        return values

    # ----
    # Tabs
    # ----
    def go_to_tab_matrix(self) -> None:
        self.tab_monitoring_matrix_link.click()

    def go_to_tab_product_classifier(self) -> None:
        self.tab_monitoring_product_classifier_link.click()

    def go_to_tab_sales(self) -> None:
        self.tab_monitoring_sales_link.click()

    def go_to_tab_realization(self) -> None:
        self.tab_monitoring_realization_link.click()

    def _tab_locator_by_key(self, key: str) -> Locator:
        key = key.lower()
        if key in {"matrix", "monitoring-matrix"}:
            return self.tab_monitoring_matrix_link
        if key in {"product-classifier", "classifier"}:
            return self.tab_monitoring_product_classifier_link
        if key in {"sales"}:
            return self.tab_monitoring_sales_link
        if key in {"realization"}:
            return self.tab_monitoring_realization_link
        raise ValueError(f"Unknown tab key: {key}")

    def is_tab_active(self, key: str) -> bool:
        """
        Check if tab is active using aria-selected.
        """
        tab = self._tab_locator_by_key(key)
        if tab.count() == 0:
            return False
        aria_selected = tab.get_attribute("aria-selected")
        return aria_selected == "true"

    # ----------
    # Assertions
    # ----------
    def assert_basic_layout_loaded(self) -> None:
        """
        Basic smoke-level assertion: navbar, tabs, filter and tree are visible,
        and the table is rendered.
        """
        # If we were redirected to the authorization page, consider the user
        # unauthorised for this run and skip UI checks instead of failing.
        if "authorization" in self.page.url:
            pytest.skip("User is not authorized for Monitoring Matrix; redirected to authorization page")

        self.navbar.check_visible()

        expect(self.tab_monitoring_matrix_link).to_be_visible()
        expect(self.filter_matrix).to_be_visible()
        expect(self.tree_zone_expand_button).to_be_visible()
        expect(self.table).to_be_visible()

    def assert_headers_contain(self, expected_subset: List[str]) -> None:
        """
        Check that mandatory columns are present in the table header.
        """
        headers = self.get_table_headers()
        for expected in expected_subset:
            assert any(expected in header for header in headers), (
                f"Expected header containing '{expected}' not found in {headers}"
            )

    def assert_filter_applied(self, key_column_pattern: Pattern[str], expected_pattern: Pattern[str]) -> None:
        """
        Verify that after applying a filter, values in the key column
        match the expected pattern.
        """
        headers = self.get_table_headers()
        key_index = None
        for idx, header in enumerate(headers):
            if re.search(key_column_pattern, header):
                key_index = idx
                break

        assert key_index is not None, f"Key column pattern {key_column_pattern.pattern!r} not found in headers {headers}"

        if self.rows_count() == 0:
            return

        first_data_row = self.table_rows.nth(1)
        cell = first_data_row.get_by_role("cell").nth(key_index)
        value = cell.inner_text().strip()
        assert re.search(
            expected_pattern, value
        ), f"Value {value!r} in key column does not match pattern {expected_pattern.pattern!r}"

