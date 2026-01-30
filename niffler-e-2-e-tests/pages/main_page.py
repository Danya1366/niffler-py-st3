from playwright.sync_api import Page

class MainPage:
    def __init__(self, page: Page):
        self.page = page

        self.add_new_spend_btn = page.locator('[href="/spending"]')
        self.statistics_container = page.locator('[id="legend-container"]')

    def remove_all_spends(self):
        self.page.get_by_role("checkbox", name="select all rows").check()
        self.page.locator('[id="delete"]').click()
        self.page.get_by_role("button", name="Delete").click()
