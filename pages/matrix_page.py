from components.navigation.navbar_component import NavbarComponent
from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class MatrixPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.navbar = NavbarComponent(page)

        self.tab_monitoring_matrix_link = page.get_by_test_id('nav-tab-item-monitoring-matrix')
        self.tab_monitoring_product_classifier_link = page.get_by_test_id('nav-tab-item-monitoring-product-classifier')
        self.tab_monitoring_sales_link = page.get_by_test_id('nav-tab-item-monitoring-sales')
        self.tab_monitoring_realization_link = page.get_by_test_id('nav-tab-item-monitoring-realization')

        self.filter_matrix = page.get_by_test_id('filter-select')

        self.tree_zone_expand_button = page.get_by_test_id('expand-button')

    def check_visible_menu_navbar(self):
        self.navbar.check_visible()

    def fill_filter_matrix(
            self,
            index: int
    ):
        self.filter_matrix.nth(index).click()


