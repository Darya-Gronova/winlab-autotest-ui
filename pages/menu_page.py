from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class MenuPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.monitoring_link = page.get_by_test_id('nav-item-monitoring')
        self.object_link = page.get_by_test_id('nav-item-objects')
        self.directory_link = page.get_by_test_id('nav-item-directory')
        self.wrong_menu_visible = page.locator('//*[@id="root"]/div/div/div/header/div[2]/div[1]/ul')

    def click_menu_link(self):
        self.monitoring_link.click()
        self.object_link.click()
        self.directory_link.click()

    def check_visible_menu_link(self):
        expect(self.wrong_menu_visible).to_be_visible()