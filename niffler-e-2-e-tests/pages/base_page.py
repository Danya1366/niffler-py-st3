from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def wait_for_load(self, timeout: int = 30000):
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url