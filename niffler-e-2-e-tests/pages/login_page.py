from playwright.sync_api import expect, Page
from .base_page import BasePage

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.get_by_placeholder('Type your username')
        self.password_input = page.get_by_placeholder('Type your password')
        self.btn_submit = page.locator('.form__submit')


class RegisterPage:
    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.locator('[id="username"]')
        self.password_input = page.locator('[id="password"]')
        self.password_submit_input = page.locator('[id="passwordSubmit"]')
        self.submit_btn = page.locator('.form__submit')
        self.sgn_in_btn = page.locator('.form_sign-in')


    # def navigate_to_login(self):
    #     self.goto(self.URL)
    #     self.wait_for_load()
    #     return self
    #
    # def verify_form_visible(self):
    #     expect(self.form_password).to_be_visible()
    #     expect(self.form_username).to_be_visible()
    #     expect(self.btn_submit).to_be_visible()
    #     return self
    #
    # def login(self, username: str, password: str):
    #     self.form_username.fill(username)
    #     self.form_password.fill(password)
    #     self.btn_submit.click()
    #     return self