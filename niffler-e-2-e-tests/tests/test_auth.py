from playwright.sync_api import expect
from conftest import app_user, main_page
from marks import Pages
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from faker import Faker

from pages.main_page import MainPage


def test_sign_up_passwords_dont_match(page, frontend_url):
    fake = Faker()
    fake_username = fake.name()
    fake_password = fake.password()
    fake_submit_password = fake.password()
    page.goto(frontend_url)
    page.locator('[href="/register"]').click()
    register_page = RegisterPage(page)
    register_page.register_new_user(fake_username, fake_password, fake_submit_password)

    expect(page.locator('[class="form__error"]')).to_contain_text('Passwords should be equal')


def test_create_new_user(page, frontend_url):
    fake = Faker()
    fake_username = fake.name()
    fake_password = fake.password()
    page.goto(frontend_url)
    main_page = MainPage(page)
    register_page = main_page.go_to_register()
    register_page.register_new_user(fake_username, fake_password, fake_password)

    login_page = register_page.click_login()
    login_page \
        .fill_user_creds(fake_username, fake_password) \
        .btn_submit.click()
    expect(page).to_have_url('http://frontend.niffler.dc/main')
    expect(page.get_by_text("History of Spendings")).to_be_visible()


def test_navigate_to_login_from_registration(page, frontend_url):
    page.goto(frontend_url)
    page.locator('[href="/register"]').click()
    main_page = RegisterPage(page)
    main_page.register_log_in_btn.click()
    expect(page).to_have_url('http://auth.niffler.dc:9000/login')


def test_valid_auth(page, app_user, frontend_url):
    username, userpassword = app_user
    page.goto(frontend_url)

    login_page = LoginPage(page)
    login_page.fill_user_creds(username, userpassword)
    expect(login_page.btn_submit).to_be_visible()
    login_page.btn_submit.click()
    expect(page).to_have_url('http://frontend.niffler.dc/main')


def test_invalid_username_auth(page, app_user, frontend_url):
    fake = Faker()
    username, userpassword = app_user
    invalid_password = fake.password()
    page.goto(frontend_url)
    login_page = LoginPage(page)
    login_page.fill_user_creds(username, invalid_password)
    expect(login_page.btn_submit).to_be_visible()
    login_page.btn_submit.click()

    msg_error = page.locator('.form__error')
    expect(msg_error).to_be_visible()


def test_invalid_password_auth(page, app_user, frontend_url):
    fake = Faker()
    username, password = app_user
    invalid_password = fake.password()

    page.goto(frontend_url)
    login_page = LoginPage(page)
    login_page.fill_user_creds(username, invalid_password)
    login_page.click_btn_submit()
    login_page.expect_msg_error()


def test_no_values_auth(page, frontend_url):
    page.goto(frontend_url)

    form_username = page.get_by_placeholder('Type your username')
    form_password = page.get_by_placeholder('Type your password')

    expect(form_password).to_be_visible()
    expect(form_username).to_be_visible()

    btn_submit = page.locator('.form__submit')

    expect(btn_submit).to_be_visible()

    btn_submit.click()


@Pages.main_page
def test_logout(page):
    main_page = MainPage(page)
    main_page.menu_btn.click()
    main_page.sign_out_btn.click()
    main_page.form_logout_btn.click()
    expect(page).to_have_url('http://auth.niffler.dc:9000/login')


@Pages.main_page
def test_dont_logout(page, frontend_url):
    main_page = MainPage(page)
    main_page.menu_btn.click()
    main_page.sign_out_btn.click()
    main_page.form_close_btn.click()
    expect(page).to_have_url(f"{frontend_url}/")
