import allure
from playwright.sync_api import expect
from marks import Pages
from faker import Faker

fake = Faker()


@allure.feature('Регистрация')
class TestRegistration:
    @allure.title('Не валидный submit password при регистрации')
    @Pages.open_login_page
    def test_sign_up_passwords_dont_match(self, login_page, register_page):
        fake_username = fake.name()
        fake_password = fake.password()
        fake_submit_password = fake.password()

        login_page.click_register_btn()
        register_page.register_new_user(fake_username, fake_password, fake_submit_password)
        register_page.expect_form_error()

    @allure.title('Cоздание нового пользователя')
    @Pages.open_login_page
    def test_create_new_user(self, login_page, register_page, envs):
        fake_username = fake.name()
        fake_password = fake.password()

        login_page.click_register_btn()
        register_page.register_new_user(fake_username, fake_password, fake_password)
        login_page = register_page.click_login()
        login_page.log_in(fake_username, fake_password, envs)

    @allure.title('Переход к окну авторизации из окна регистрации')
    @Pages.open_login_page
    def test_navigate_to_login_from_registration(self, login_page, register_page):
        login_page.click_register_btn()
        register_page.btn_log_in_registration()


@allure.feature('Авторизация')
class TestAuth:
    @allure.title('Авторизация с валидными данными')
    @Pages.open_login_page
    def test_valid_auth(self, login_page, envs):
        login_page.log_in(envs.test_username, envs.test_password, envs)

    @allure.title('Авторизация с невалидным именем пользователя')
    @Pages.open_login_page
    def test_invalid_username_auth(self, envs, login_page):
        invalid_password = fake.password()

        login_page.fill_user_creds(envs.test_username, invalid_password)
        expect(login_page.btn_submit).to_be_visible()
        login_page.btn_submit.click()
        expect(login_page.msg_error).to_be_visible()

    @allure.title('Авторизация с неверным паролем')
    @Pages.open_login_page
    def test_invalid_password_auth(self, envs, login_page):
        invalid_password = fake.password()
        login_page.fill_user_creds(envs.test_username, invalid_password)
        login_page.click_btn_submit()
        login_page.expect_msg_error()

    @allure.title('Авторизация с пустыми значениями для полей')
    @Pages.open_login_page
    def test_no_values_auth(self, page, envs, login_page):
        login_page.click_btn_submit()
        expect(page).to_have_url(envs.login_url)

    @allure.story("Логаут")
    @allure.title('Успешный выход из системы')
    @Pages.main_page
    def test_logout(self, envs, main_page):
        main_page.logot(envs)

    @allure.story("Логаут")
    @allure.title("Отмена выхода из системы")
    @Pages.main_page
    def test_dont_logout(self, envs, main_page):
        main_page.dont_logout(envs)
