from playwright.sync_api import expect, Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.get_by_placeholder('Type your username')
        self.password_input = page.get_by_placeholder('Type your password')
        self.btn_submit = page.locator('.form__submit')


class RegisterPage:
    def __init__(self, page: Page):
        self.page = page
        self.register_url = 'http://auth.niffler.dc:9000/register'

        self.username_input = page.locator('[id="username"]')
        self.password_input = page.locator('[id="password"]')
        self.password_submit_input = page.locator('[id="passwordSubmit"]')
        self.submit_btn = page.locator('.form__submit')
        self.sgn_in_btn = page.locator('.form_sign-in')


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
