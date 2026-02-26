import re

from playwright.sync_api import Page, expect
from components.base_component import BaseComponent


class NavbarComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        # Prefer semantic roles and stable text over brittle test ids.
        # If the implementation keeps test ids, these locators will still
        # resolve correctly by accessible name.
        self.app_title_monitoring = page.get_by_role(
            "link",
            name=re.compile("Мониторинг", re.IGNORECASE),
        )
        self.app_title_objects = page.get_by_role(
            "link",
            name=re.compile("Объекты", re.IGNORECASE),
        )
        self.app_title_directory = page.get_by_role(
            "link",
            name=re.compile("Справочники", re.IGNORECASE),
        )

    def check_visible(self):
        expect(self.app_title_monitoring).to_be_visible()
        expect(self.app_title_monitoring).to_contain_text("Мониторинг")

        expect(self.app_title_objects).to_be_visible()
        expect(self.app_title_objects).to_contain_text("Объекты")

        expect(self.app_title_directory).to_be_visible()
        expect(self.app_title_directory).to_contain_text("Справочники")

    def check_menu_link(self):
        self.check_visible()
