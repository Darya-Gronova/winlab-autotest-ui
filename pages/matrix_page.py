from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class MatrixPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.tab_monitoring_matrix_link = page.get_by_test_id('nav-tab-item-monitoring-matrix')
        self.tab_monitoring_product_classifier_link = page.get_by_test_id('nav-tab-item-monitoring-product-classifier')
        self.tab_monitoring_sales_link = page.get_by_test_id('nav-tab-item-monitoring-sales')
        self.tab_monitoring_realization_link = page.get_by_test_id('nav-tab-item-monitoring-realization')

        self.filter_division = page.get_by_test_id('filter-select')
