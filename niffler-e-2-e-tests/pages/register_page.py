import allure
from playwright.sync_api import expect, Page
from pages.login_page import LoginPage


class RegisterPage:
    def __init__(self, page: Page, frontend_url: str):
        self.page = page
        self.frontend_url = frontend_url

        self.username_input = page.locator('[id="username"]')
        self.password_input = page.locator('[id="password"]')
        self.password_submit_input = page.locator('[id="passwordSubmit"]')
        self.submit_btn = page.locator('.form__submit')
        self.sgn_in_btn = page.locator('.form_sign-in')
        self.register_log_in_btn = page.get_by_role("link", name="Log in")
        self.form_error = page.locator('[class="form__error"]')

    def password_input_fill(self, password: str):
        with allure.step('Ввести пароль'):
            self.password_input.click()
            self.password_input.fill(password)
            return self

    def username_input_fill(self, username: str):
        with allure.step('Ввести логин'):
            self.username_input.click()
            self.username_input.fill(username)
            return self

    def password_submit_input_fill(self, password: str):
        with allure.step('Повторить пароль'):
            self.password_submit_input.click()
            self.password_submit_input.fill(password)
            return self

    def click_login(self):
        with allure.step('Нажать на кнопку log in'):
            expect(self.page.locator('.form__paragraph_success')).to_be_visible()
            expect(self.sgn_in_btn).to_be_visible()
            self.sgn_in_btn.click()
            return LoginPage(self.page, self.frontend_url)

    def register_new_user(self, username: str, password: str, submit_password: str):
        with allure.step('Зарегестрировать нового пользователя'):
            expect(self.username_input).to_be_visible()
            expect(self.password_input).to_be_visible()
            expect(self.password_submit_input).to_be_visible()

            self.username_input.fill(username)
            self.password_input.fill(password)
            self.password_submit_input.fill(submit_password)
            self.submit_btn.click()
            return self

    def expect_form_error(self):
        with allure.step('Проверить отображение форму ошибки'):
            expect(self.form_error).to_contain_text('Passwords should be equal')
            return self

    def btn_log_in_registration(self):
        with allure.step('Нажать на кнопку log in на странице регистрации'):
            self.register_log_in_btn.click()
            expect(self.page).to_have_url("http://auth.niffler.dc:9000/login")
            return self
