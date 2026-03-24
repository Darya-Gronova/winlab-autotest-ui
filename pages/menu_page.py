from components.navigation.navbar_component import NavbarComponent
from pages.base_page import BasePage
from playwright.sync_api import Locator, Page, expect


class MenuPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.navbar = NavbarComponent(page)

        self.monitoring_link: Locator = page.get_by_test_id("nav-item-monitoring")
        self.object_link: Locator = page.get_by_test_id("nav-item-objects")
        self.directory_link: Locator = page.get_by_test_id("nav-item-directory")

    def click_menu_link(self):
        self.monitoring_link.click()
        self.object_link.click()
        self.directory_link.click()

    def check_visible_menu_link(self):
        # Delegate to the shared Navbar component which already validates
        # that all main navigation links are visible and have expected text.
        self.navbar.check_visible()

    def check_menu_link(self):
        # Ensure main navigation links are visible after successful authorization
        self.navbar.check_menu_link()
        expect(self.monitoring_link).to_be_visible()
        expect(self.object_link).to_be_visible()
        expect(self.directory_link).to_be_visible()