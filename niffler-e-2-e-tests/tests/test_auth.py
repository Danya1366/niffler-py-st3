from playwright.sync_api import expect
from marks import Pages
from faker import Faker

fake = Faker()


@Pages.open_login_page
def test_sign_up_passwords_dont_match(login_page, register_page):
    fake_username = fake.name()
    fake_password = fake.password()
    fake_submit_password = fake.password()

    login_page.click_register_btn()
    register_page.register_new_user(fake_username, fake_password, fake_submit_password)
    register_page.expect_form_error()


@Pages.open_login_page
def test_create_new_user(login_page, register_page, envs):
    fake_username = fake.name()
    fake_password = fake.password()

    login_page.click_register_btn()
    register_page.register_new_user(fake_username, fake_password, fake_password)
    login_page = register_page.click_login()
    login_page.log_in(fake_username, fake_password, envs)


@Pages.open_login_page
def test_navigate_to_login_from_registration(login_page, register_page):
    login_page.click_register_btn()
    register_page.btn_log_in_registration()


@Pages.open_login_page
def test_valid_auth(login_page, envs):
    login_page.log_in(envs.test_username, envs.test_password, envs)


@Pages.open_login_page
def test_invalid_username_auth(envs, login_page):
    invalid_password = fake.password()

    login_page.fill_user_creds(envs.test_username, invalid_password)
    expect(login_page.btn_submit).to_be_visible()
    login_page.btn_submit.click()
    expect(login_page.msg_error).to_be_visible()


@Pages.open_login_page
def test_invalid_password_auth(envs, login_page):
    invalid_password = fake.password()
    login_page.fill_user_creds(envs.test_username, invalid_password)
    login_page.click_btn_submit()
    login_page.expect_msg_error()


@Pages.open_login_page
def test_no_values_auth(page, envs, login_page):
    login_page.click_btn_submit()
    expect(page).to_have_url(envs.login_url)


@Pages.main_page
def test_logout(envs, main_page):
    main_page.logot(envs)


@Pages.main_page
def test_dont_logout(envs, main_page):
    main_page.dont_logout(envs)
