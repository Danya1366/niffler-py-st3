from playwright.sync_api import expect
from marks import Pages
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from faker import Faker

from pages.main_page import MainPage

@Pages.open_login_page
def test_sign_up_passwords_dont_match(page, login_page, register_page):
    fake = Faker()
    fake_username = fake.name()
    fake_password = fake.password()
    fake_submit_password = fake.password()
    login_page.click_register_btn()
    register_page.register_new_user(fake_username, fake_password, fake_submit_password)

    expect(page.locator('[class="form__error"]')).to_contain_text('Passwords should be equal')

@Pages.open_login_page
def test_create_new_user(page, login_page, register_page):
    fake = Faker()
    fake_username = fake.name()
    fake_password = fake.password()
    login_page.click_register_btn()
    register_page.register_new_user(fake_username, fake_password, fake_password)
    login_page = register_page.click_login()
    login_page \
        .fill_user_creds(fake_username, fake_password) \
        .btn_submit.click()
    expect(page).to_have_url('http://frontend.niffler.dc/main')
    expect(page.get_by_text("History of Spendings")).to_be_visible()

@Pages.open_login_page
def test_navigate_to_login_from_registration(page, login_page, register_page):
    login_page.click_register_btn()
    main_page = RegisterPage(page)
    main_page.register_log_in_btn.click()
    expect(page).to_have_url('http://auth.niffler.dc:9000/login')

@Pages.open_login_page
def test_valid_auth(login_page, envs, page):
    login_page.fill_user_creds(envs.test_username, envs.test_password)
    expect(login_page.btn_submit).to_be_visible()
    login_page.btn_submit.click()
    expect(page).to_have_url('http://frontend.niffler.dc/main')

@Pages.open_login_page
def test_invalid_username_auth(page, envs, login_page):
    fake = Faker()
    invalid_password = fake.password()
    login_page.fill_user_creds(envs.test_username, invalid_password)
    expect(login_page.btn_submit).to_be_visible()
    login_page.btn_submit.click()

    msg_error = page.locator('.form__error')
    expect(msg_error).to_be_visible()

@Pages.open_login_page
def test_invalid_password_auth(page, envs, login_page):
    fake = Faker()
    invalid_password = fake.password()
    login_page.fill_user_creds(envs.test_username, invalid_password)
    login_page.click_btn_submit()
    login_page.expect_msg_error()

@Pages.open_login_page
def test_no_values_auth(page, envs, login_page):
    login_page.click_btn_submit()
    expect(page).to_have_url('http://auth.niffler.dc:9000/login')


@Pages.main_page
def test_logout(page):
    main_page = MainPage(page)
    main_page.menu_btn.click()
    main_page.sign_out_btn.click()
    main_page.form_logout_btn.click()
    expect(page).to_have_url('http://auth.niffler.dc:9000/login')


@Pages.main_page
def test_dont_logout(page,envs):
    main_page = MainPage(page)
    main_page.menu_btn.click()
    main_page.sign_out_btn.click()
    main_page.form_close_btn.click()
    expect(page).to_have_url(f"{envs.frontend_url}/")
