from playwright.sync_api import Page, expect
from datetime import datetime, timedelta

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

        yesterday = datetime.now() - timedelta(days=1)
        self.yesterday_day = str(yesterday.day)

    def navigate_to_spending_page(self):
        self.go_to(self.front_url)
        self.wait_for_load()

    def add_amount(self, amount: str):
        self.amount_input_field.wait_for(state="visible")
        self.amount_input_field.click()
        self.amount_input_field.press('Backspace')
        self.amount_input_field.fill(str(amount))
        return self

    def add_category(self, category: str):
        self.category_input_field.wait_for(state="visible")
        self.category_input_field.click()
        self.category_input_field.fill(str(category))
        return self

    def set_the_date_to_yesterday(self):
        self.calendar_icon.wait_for(state="visible")
        self.calendar_icon.click()
        self.page.get_by_role("gridcell", name=str(self.yesterday_day), exact=True).click()
        return self

    def add_description(self, description: str):
        self.calendar_icon.wait_for(state="visible")
        self.description_field.click()
        self.description_field.fill(str(description))
        return self

    def add_new_spending(self, amount, category, description):
        self.amount_input_field.fill(amount)
        self.category_input_field.fill(category)
        self.description_field.fill(description)
        self.btn_save.click()
        self.page.get_by_text("New spending is successfully created").wait_for(state='visible')
        return self

    def update_amount(self, edited_amount: str):
        expect(self.amount_input_field).to_be_visible()
        self.amount_input_field.click()
        self.amount_input_field.press("ControlOrMeta+A")
        self.amount_input_field.press('Backspace')
        self.amount_input_field.fill(edited_amount)
        return self

    def update_category(self, edited_category: str):
        expect(self.category_input_field).to_be_visible()
        self.category_input_field.click()
        self.category_input_field.fill(edited_category)
        return self

    def add_new_spending_with_last_date(self, amount, category, description):
        self.amount_input_field.fill(amount)
        self.category_input_field.fill(category)
        self.description_field.fill(description)
        self.calendar_icon.wait_for(state="visible")
        self.calendar_icon.click()
        self.page.get_by_role("gridcell", name=str(self.yesterday_day), exact=True).click()

        return self

