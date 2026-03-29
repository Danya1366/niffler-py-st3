import allure
from playwright.sync_api import Page, expect
from utils.datatime_util import get_past_date_str

from pages.base_page import BasePage


class SpendingPage(BasePage):
    def __init__(self, page: Page, frontend_url):
        super().__init__(page)
        self.page = page
        self.front_url = frontend_url

        self.amount_input_field = page.locator('input[name="amount"]')
        self.category_input_field = page.locator('input[name="category"]')
        self.calendar_icon = page.locator('img[alt="Calendar"]')
        self.description_field = page.locator('input[name="description"]')
        self.btn_save = page.locator('#save')

        self.yesterday_day = get_past_date_str()

    @allure.step('Добавить описание')
    def add_description(self, description: str):
        self.calendar_icon.wait_for(state="visible")
        self.description_field.click()
        self.description_field.fill(str(description))
        return self

    @allure.step('Добавить новую трату UI')
    def add_new_spending(self, amount, category, description):
        self.amount_input_field.fill(amount)
        self.category_input_field.fill(category)
        self.description_field.fill(description)
        self.btn_save.click()
        self.page.get_by_text("New spending is successfully created").wait_for(state='visible')
        return self

    @allure.step('Обновить amount')
    def update_amount(self, edited_amount: str):
        expect(self.amount_input_field).to_be_visible()
        self.amount_input_field.click()
        self.amount_input_field.press("ControlOrMeta+A")
        self.amount_input_field.press('Backspace')
        self.amount_input_field.fill(edited_amount)
        return self

    @allure.step('Обновить категорию')
    def update_category(self, edited_category: str):
        expect(self.category_input_field).to_be_visible()
        self.category_input_field.click()
        self.category_input_field.fill(edited_category)
        return self

    @allure.step('Добавить новую трауту за "Вчера"')
    def add_new_spending_with_last_date(self, amount, category, description):
        self.amount_input_field.fill(amount)
        self.category_input_field.fill(category)
        self.description_field.fill(description)
        self.calendar_icon.wait_for(state="visible")
        self.calendar_icon.click()
        self.page.get_by_role("gridcell", name=str(self.yesterday_day), exact=True).click()
        return self

    @allure.step('Нажать на кнопку "Сохранить"')
    def click_save_btn(self, envs):
        self.btn_save.click()
        expect(self.page).to_have_url(envs.main_page_url)
        self.page.wait_for_load_state()
        return self
