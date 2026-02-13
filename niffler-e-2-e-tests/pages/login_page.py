from playwright.sync_api import expect, Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.get_by_placeholder('Type your username')
        self.password_input = page.get_by_placeholder('Type your password')
        self.btn_submit = page.locator('.form__submit')
        self.msg_error = page.locator('.form__error')

    def fill_user_creds(self, username: str, password: str):
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        self.username_input.fill(username)
        self.password_input.fill(password)
        return self

    def expect_msg_error(self):
        expect(self.msg_error).to_be_visible()
        return self

    def click_btn_submit(self):
        expect(self.btn_submit).to_be_visible()
        self.btn_submit.click()

