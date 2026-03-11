import allure

from fixtures.pages_fixtures import main_page
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

        with allure.step("Переход на страницу регистрации"):
            login_page.click_register_btn()
        with allure.step("Регистрация нового пользователя"):
            register_page.register_new_user(fake_username, fake_password, fake_password)
        with allure.step("Переход на страницу логина"):
            login_page = register_page.click_login()
        with allure.step("Авторизация после регистрации"):
            login_page.log_in(fake_username, fake_password)
        with allure.step("Проверка успешной авторизации"):
            assert login_page.is_history_block_visible()


@allure.feature('Авторизация')
class TestAuth:
    @allure.title('Авторизация с валидными данными')
    @Pages.open_login_page
    def test_valid_auth(self, login_page, envs):
        login_page.log_in(envs.test_username, envs.test_password)
        assert login_page.is_history_block_visible()

    @allure.title('Авторизация с невалидным именем пользователя')
    @Pages.open_login_page
    def test_invalid_username_auth(self, envs, login_page):
        invalid_username = fake.password()
        login_page.fill_user_creds(invalid_username, envs.test_password)
        login_page.btn_submit.click()
        assert login_page.is_error_message_visible()


@allure.title('Авторизация с неверным паролем')
@Pages.open_login_page
def test_invalid_password_auth(envs, login_page):
    invalid_password = fake.password()
    login_page.fill_user_creds(envs.test_username, invalid_password)
    login_page.click_btn_submit()
    assert login_page.is_error_message_visible()


@allure.title('Авторизация с пустыми значениями для полей')
@Pages.open_login_page
def test_no_values_auth(envs, login_page):
    login_page.click_btn_submit()
    assert login_page.is_login_page_open(envs.login_url)


@allure.story("Логаут")
@allure.title('Успешный выход из системы')
@Pages.open_main_page
def test_logout(envs, main_page):
    main_page.logout(envs.login_url)
    assert main_page.is_logged_out(envs.login_url)


@allure.story("Логаут")
@allure.title("Отмена выхода из системы")
@Pages.open_main_page
def test_dont_logout(envs, main_page):
    main_page.dont_logout()
    assert main_page.dont_logged_out(envs.main_page_url)
