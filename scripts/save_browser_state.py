"""Save authenticated Playwright storage state to `browser-state.json`.

Usage:
  - Set env vars `AUTH_LOGIN` and `AUTH_PASSWORD` or edit the defaults below.
  - Run: `python scripts/save_browser_state.py`

This script opens the authorization page, fills credentials, clicks login
and saves the storage state to the project root as `browser-state.json`.
"""
from playwright.sync_api import sync_playwright
import os
import json

AUTH_LOGIN = os.environ.get('AUTH_LOGIN', 'dariak')
AUTH_PASSWORD = os.environ.get('AUTH_PASSWORD', 'r63l80AV')
AUTH_URL = 'https://devatlaskm.marketing-logic.ru/authorization'
OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'browser-state.json')


def save_state():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(AUTH_URL, wait_until='networkidle')

        # Try to fill fields using known test ids from page object
        try:
            page.get_by_test_id('login-input').fill(AUTH_LOGIN)
            page.get_by_test_id('password-input').fill(AUTH_PASSWORD)
            page.get_by_test_id('login-button').click()
        except Exception:
            # fallback: try common selectors
            try:
                page.fill('input[name="username"]', AUTH_LOGIN)
                page.fill('input[name="password"]', AUTH_PASSWORD)
                page.click('button[type="submit"]')
            except Exception as e:
                print('Could not perform login automatically:', e)

        # wait a bit for navigation / auth to complete
        page.wait_for_timeout(3000)

        storage = context.storage_state()

        out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'browser-state.json'))
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(storage, f, ensure_ascii=False, indent=2)

        print('Saved storage state to', out_path)
        browser.close()


if __name__ == '__main__':
    save_state()
