from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.register_page import RegisterPage
from pages.profile_page import ProfilePage
from pages.spending_page import SpendingPage


class MainPage(BasePage):
    def __init__(self, page: Page, frontend_url: str):
        super().__init__(page)

        self.page = page
        self.frontend_url = frontend_url

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
        self.menu = page.get_by_role("menu")

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
        expect(self.page).to_have_url(f"{self.frontend_url}/register")
        return RegisterPage(self.page)

    def go_to_profile(self):
        self.menu_btn.click()
        self.profile_btn.click()
        expect(self.page).to_have_url(f"{self.frontend_url}/profile")
        return ProfilePage(self.page)

    def go_to_spend(self):
        self.add_new_spend_btn.click()
        expect(self.page).to_have_url(f"{self.frontend_url}/spending")
        return SpendingPage(self.page, self.frontend_url)

    def expect_expense_table(self, amount, category, description):
        expect(self.statistics_container).to_contain_text(f"{category} {amount}")
        expect(self.expense_table).to_contain_text(description)
        expect(self.expense_table).to_contain_text(amount)
        expect(self.expense_table).to_contain_text(category)
        return self

    def expect_content_of_table(self, description: str):
        self.page.reload()
        expect(self.expense_table).to_be_visible()
        expect(self.expense_table).to_contain_text(description)
        return self

    def expect_content_of_table_is_empty(self, description: str):
        expect(self.container_history_of_spending).not_to_contain_text(description)
        return self

    def click_on_checkbox_with_name(self, name: str):
        self.page.get_by_role("checkbox", name=name).get_by_label("Edit spending").click()

    def expect_statics_container_for_total(self, category, amount1, amount2):
        total_amount = float(amount1) + float(amount2)
        expect(self.statistics_container).to_contain_text(f"{category} {total_amount}")

    def dont_logout(self, envs):
        self.menu_btn.click()
        self.sign_out_btn.click()
        expect(self.form_close_btn).to_be_visible()
        self.form_close_btn.click()
        expect(self.page).to_have_url(envs.main_page_url)

    def logot(self, envs):
        self.menu_btn.click()
        expect(self.menu).to_be_visible()
        self.sign_out_btn.click()
        self.form_logout_btn.click()
        expect(self.page).to_have_url(envs.login_url)
        expect(self.page.get_by_text("Log in").first).to_be_visible()
