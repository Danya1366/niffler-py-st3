import allure
from playwright.sync_api import Page, expect

from conftest import page_with_auth
from pages.base_page import BasePage
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

    @allure.step('Удалить все траты UI')
    def remove_all_spends(self):
        self.page.get_by_role("checkbox", name="select all rows").check()
        self.page.locator('[id="delete"]').click()
        self.page.get_by_role("button", name="Delete").click()
        expect(self.container_history_of_spending).to_contain_text('There are no spendings')
        return self

    @allure.step('Удалить созданную трату')
    def delete_spend(self, name: str):
        self.wait_for_load()
        self.page.get_by_role("checkbox", name=name, exact=True).click()
        self.page.locator('[id="delete"]').click()
        self.page.get_by_role("button", name="Delete").click()
        return self

    # @allure.step('Перейти в регистрацию')
    # def go_to_register(self):
    #     expect(self.register_form).to_be_visible()
    #     expect(self.register_form).to_contain_text('Create new account')
    #     self.register_form.click()
    #     expect(self.page).to_have_url(f"{self.frontend_url}/register")
    #     return RegisterPage(self.page)

    @allure.step('Перейти в траты')
    def go_to_spend(self):
        self.page.reload()
        self.add_new_spend_btn.click()
        expect(self.page).to_have_url(f"{self.frontend_url}/spending")
        return SpendingPage(self.page, self.frontend_url)

    @allure.step('Проверяем статистику трат')
    def is_statistics_correct(self, category: str, amount: str) -> bool:
        self.wait_for_load()
        self.statistics_container.wait_for(state="visible", timeout=10000)
        return f"{category} {amount}" in self.statistics_container.text_content()

    @allure.step('Проверяем описание траты')
    def is_description_in_table(self, description: str) -> bool:
        self.page.reload()
        self.wait_for_load()
        return description in self.expense_table.text_content()

    @allure.step('Проверяем сумму траты')
    def is_amount_in_table(self, amount: str) -> bool:
        return amount in self.expense_table.text_content()

    @allure.step('Проверяем категорию траты')
    def is_category_in_table(self, category: str) -> bool:
        return category in self.expense_table.text_content()

    @allure.step('Проверить что в таблице трат отсутствуют данные')
    def is_description_absent_in_table(self, description: str) -> bool:
        self.wait_for_load()
        self.container_history_of_spending.wait_for(state="visible", timeout=10000)
        assert self.container_history_of_spending.is_visible()
        table_text = self.container_history_of_spending.text_content()
        return description not in table_text

    @allure.step('Нажать на чек-бокс с название ктегории')
    def click_on_checkbox_with_name(self, name: str):
        self.page.get_by_role("checkbox", name=name).get_by_label("Edit spending").click()
        return self

    @allure.step('Проверить сумму трат')
    def is_total_amount_correct(self, category: str, amount1: str, amount2: str) -> bool:
        total_amount = float(amount1) + float(amount2)
        self.statistics_container.wait_for(state="visible")
        statistics_text = self.statistics_container.text_content()
        return f"{category} {total_amount}" in statistics_text

    @allure.step('Не выполнить выход из системы по кнопке Отмена')
    def dont_logout(self):
        self.menu_btn.click()
        self.sign_out_btn.click()
        expect(self.form_close_btn).to_be_visible()
        self.form_close_btn.click()
        return self

    @allure.step('Проверка что выход не выполнен. Остались на основной странице: {main_page_url}')
    def dont_logged_out(self, main_page_url):
        return self.page.url == main_page_url

    @allure.step('Выполнить выход из системы по кнопке')
    def logout(self, login_url):
        self.menu_btn.click()
        expect(self.menu).to_be_visible()
        with self.page.expect_navigation(url=login_url):
            self.sign_out_btn.click()
            self.form_logout_btn.click()

        return self

    @allure.step('Проверка что выход выполнен. Выполнен переход на страницу логина:  {login_url}')
    def is_logged_out(self, login_url):
        return self.page.url == login_url

    @allure.step('Проверка что находимся на основной странице: {main_page_url}')
    def is_main_page_open(self, main_page_url):
        return self.page.url == main_page_url
