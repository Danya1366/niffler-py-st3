import allure
from playwright.sync_api import expect, Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page, frontend_url: str | None):
        super().__init__(page)
        self.page = page
        self.frontend_url = frontend_url

        self.username_input = page.get_by_placeholder('Type your username')
        self.password_input = page.get_by_placeholder('Type your password')
        self.btn_submit = page.locator('.form__submit')
        self.msg_error = page.locator('.form__error')
        self.registor_button = page.locator('[href="/register"]')

    def fill_user_creds(self, username: str, password: str):
        with allure.step('Заполнить учетные данные пользователя'):
            expect(self.username_input).to_be_visible()
            expect(self.password_input).to_be_visible()
            self.username_input.fill(username)
            self.password_input.fill(password)
            expect(self.btn_submit).to_be_visible()
            return self

    def expect_msg_error(self):
        with allure.step('Проверить сообщение об ошибке'):
            expect(self.msg_error).to_be_visible()
            return self

    def click_btn_submit(self):
        with allure.step('Нажать на кнопку "Подтвердить"'):
            expect(self.btn_submit).to_be_visible()
            self.btn_submit.click()
            return self

    def click_register_btn(self):
        with allure.step('Нажать на кнопку "Регистрация"'):
            from pages.register_page import RegisterPage
            expect(self.registor_button).to_be_visible()
            self.registor_button.click()
            return RegisterPage(self.page, self.frontend_url)

    def log_in(self, username, password):
        with allure.step('Авторизоваться используя учетные данные пользователя'):
            self.fill_user_creds(username, password)
            self.btn_submit.click()
            return self

    def expect_log_in(self, envs):
        with allure.step('Проверяем что авторизованны'):
            expect(self.page).to_have_url(envs.main_page_url)
            expect(self.page.get_by_text("History of Spendings")).to_be_visible()
            return self
