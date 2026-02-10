from playwright.sync_api import Page
from datetime import datetime, timedelta

class SpendingPage:
    def __init__(self, page: Page):
        self.page = page


        self.amount_input_field = page.locator('input[name="amount"]')
        self.category_input_field = page.locator('input[name="category"]')
        self.calendar_icon = page.locator('img[alt="Calendar"]')
        self.description_field = page.locator('input[name="description"]')
        self.btn_save = page.locator('#save')


        yesterday = datetime.now() - timedelta(days=1)
        self.yesterday_day = str(yesterday.day)

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

    def save_change(self):
        self.btn_save.wait_for(state="visible")
        self.btn_save.click()
        return self

