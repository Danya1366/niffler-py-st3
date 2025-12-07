from playwright.sync_api import expect
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "http://auth.niffler.dc:9000/login"
    def __init__(self, page):
        super().__init__(page)
        self.goto(self.URL)
        self.form_username = page.get_by_placeholder('Type your username')
        self.form_password = page.get_by_placeholder('Type your password')
        self.btn_submit = page.locator('.form__submit')

    def navigate_to_login(self):
        self.goto(self.URL)
        self.wait_for_load()
        return self

    def verify_form_visible(self):
        expect(self.form_password).to_be_visible()
        expect(self.form_username).to_be_visible()
        expect(self.btn_submit).to_be_visible()
        return self

    def login(self, username: str, password: str):
        self.form_username.fill(username)
        self.form_password.fill(password)
        self.btn_submit.click()
        return self