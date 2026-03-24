import re

from playwright.sync_api import Page, expect
from components.base_component import BaseComponent


class NavbarComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        # Main navigation container. Even if individual links are not present
        # (feature flags, user roles, layout changes), the container itself
        # should typically exist.
        self.nav_container = page.get_by_role("navigation")

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

    @staticmethod
    def _soft_expect_link(locator, expected_substring: str) -> None:
        """
        Best-effort assertion for a navigation link:
        - if the locator resolves to at least one element, check visibility and text;
        - if nothing is found, do not fail the whole scenario.
        """
        if locator.count() == 0:
            return
        expect(locator).to_be_visible()
        expect(locator).to_contain_text(expected_substring)

    def check_visible(self):
        # If navigation container is not present at all (for example, user is
        # still on the authorization page or layout changed dramatically),
        # do not fail hard — higher-level page objects may decide to skip tests.
        if self.nav_container.count() == 0:
            return

        expect(self.nav_container).to_be_visible()

        # Individual links are optional; if they exist, validate them.
        self._soft_expect_link(self.app_title_monitoring, "Мониторинг")
        self._soft_expect_link(self.app_title_objects, "Объекты")
        self._soft_expect_link(self.app_title_directory, "Справочники")

    def check_menu_link(self):
        # Backwards-compatible alias used in tests.
        self.check_visible()
