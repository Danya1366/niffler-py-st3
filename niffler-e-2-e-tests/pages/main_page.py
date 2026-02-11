from playwright.sync_api import Page, expect

from pages.register_page import RegisterPage
from pages.profile_page import ProfilePage
from pages.spending_page import SpendingPage

from datetime import datetime, timedelta


class MainPage:
    def __init__(self, page: Page):
        self.page = page

        self.add_new_spend_btn = page.locator('[href="/spending"]')
        self.statistics_container = page.locator('[id="legend-container"]')
        self.expense_table = page.locator('[aria-labelledby="tableTitle"]')
        self.container_history_of_spending = page.locator('[id="spendings"]')
        self.register_form = page.locator('[href="/register"]')
        self.menu_btn = page.locator('[aria-label="Menu"]')
        self.sign_out_btn = page.get_by_role("menuitem", name="Sign out")
        self.form_logout_btn = page.get_by_role('button', name="Log out")
        self.form_close_btn = page.get_by_role("button", name="Close")
        self.profile_btn = page.locator('[href="/profile"]')

    def remove_all_spends(self):
        self.page.get_by_role("checkbox", name="select all rows").check()
        self.page.locator('[id="delete"]').click()
        self.page.get_by_role("button", name="Delete").click()
        expect(self.container_history_of_spending).to_contain_text('There are no spendings')
        return self

    def delete_spend(self, name: str):
        self.page.get_by_role("checkbox", name=name, exact=True).click()
        self.page.locator('[id="delete"]').click()
        self.page.get_by_role("button", name="Delete").click()
        return self

    def go_to_register(self):
        expect(self.register_form).to_be_visible()
        expect(self.register_form).to_contain_text('Create new account')
        self.register_form.click()
        expect(self.page).to_have_url('http://auth.niffler.dc:9000/register')
        return RegisterPage(self.page)

    def go_to_profile(self):
        self.menu_btn.click()
        self.profile_btn.click()
        expect(self.page).to_have_url('http://frontend.niffler.dc/profile')
        return ProfilePage(self.page)

    def go_to_spend(self, frontend_url):
        self.frontend_url = frontend_url
        self.add_new_spend_btn.click()
        expect(self.page).to_have_url('http://frontend.niffler.dc/spending')
        return SpendingPage(self.page, self.frontend_url)

    def expect_expense_table(self, amount, category, description):
        expect(self.statistics_container).to_contain_text(f"{category} {amount}")
        expect(self.expense_table).to_contain_text(description)
        expect(self.expense_table).to_contain_text(amount)
        expect(self.expense_table).to_contain_text(category)
        return self
