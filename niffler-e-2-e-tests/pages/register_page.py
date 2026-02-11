from playwright.sync_api import expect, Page
from pages.login_page import LoginPage


class RegisterPage:
    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.locator('[id="username"]')
        self.password_input = page.locator('[id="password"]')
        self.password_submit_input = page.locator('[id="passwordSubmit"]')
        self.submit_btn = page.locator('.form__submit')
        self.sgn_in_btn = page.locator('.form_sign-in')
        self.register_log_in_btn = page.get_by_role("link", name="Log in")

    def password_input_fill(self, password: str):
        self.password_input.click()
        self.password_input.fill(password)
        return self

    def username_input_fill(self, username: str):
        self.username_input.click()
        self.username_input.fill(username)
        return self

    def password_submit_input_fill(self, password: str):
        self.password_submit_input.click()
        self.password_submit_input.fill(password)
        return self

    def click_login(self):
        expect(self.page.locator('.form__paragraph_success')).to_be_visible()
        expect(self.sgn_in_btn).to_be_visible()
        self.sgn_in_btn.click()
        return LoginPage(self.page)

    def register_new_user(self, username: str, password: str, submit_password: str):
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.password_submit_input).to_be_visible()

        self.username_input.fill(username)
        self.password_input.fill(password)
        self.password_submit_input.fill(submit_password)
        self.submit_btn.click()
        return self