from playwright.sync_api import expect
from conftest import app_user
from marks import Pages
from pages.login_page import LoginPage, RegisterPage
from faker import Faker


def test_page_title(page, frontend_url):
    page.goto(frontend_url)
    expect(page.locator('.header')).to_contain_text("Log in")


def test_1(page, frontend_url, app_user):
    username, password = app_user
    page.goto(frontend_url)
    login_page = LoginPage(page)
    login_page.username_input.fill(username)
    login_page.password_input.fill(password)
    login_page.btn_submit.click()
    expect(page).to_have_url('http://frontend.niffler.dc/main')
    expect(page.get_by_text("History of Spendings")).to_be_visible()


def test_sign_up_passwords_dont_match(page, frontend_url):
    page.goto(frontend_url)
    page.locator('[href="/register"]').click()
    register_page = RegisterPage(page)

    register_page.username_input_fill('Тестовый')
    register_page.password_input_fill('123321')
    register_page.password_submit_input_fill('321123')
    register_page.submit_btn.click()

    expect(page.locator('[class="form__error"]')).to_contain_text('Passwords should be equal')


def test_create_new_user(page, frontend_url):
    fake = Faker()
    fake_username = fake.name()
    fake_password = fake.password()
    page.goto(frontend_url)

    register_form = page.locator('[href="/register"]')
    expect(register_form).to_be_visible()
    expect(register_form).to_contain_text('Create new account')
    register_form.click()
    expect(page).to_have_url('http://auth.niffler.dc:9000/register')

    register_page = RegisterPage(page)

    expect(register_page.username_input).to_be_visible()
    expect(register_page.password_input).to_be_visible()
    expect(register_page.password_submit_input).to_be_visible()

    register_page.username_input.fill(fake_username)
    register_page.password_input.fill(fake_password)
    register_page.password_submit_input.fill(fake_password)
    register_page.submit_btn.click()

    expect(page.locator('.form__paragraph_success')).to_be_visible()
    expect(register_page.sgn_in_btn).to_be_visible()

    register_page.sgn_in_btn.click()

    login_page = LoginPage(page)
    login_page.username_input.fill(fake_username)
    login_page.password_input.fill(fake_password)
    login_page.btn_submit.click()
    expect(page).to_have_url('http://frontend.niffler.dc/main')
    expect(page.get_by_text("History of Spendings")).to_be_visible()


def test_valid_auth(page, app_user):
    username, userpassword = app_user
    page.goto("http://auth.niffler.dc:9000/login")

    form_username = page.get_by_placeholder('Type your username')
    form_password = page.get_by_placeholder('Type your password')

    expect(form_password).to_be_visible()
    expect(form_username).to_be_visible()

    form_username.fill(username)
    form_password.fill(userpassword)
    btn_submit = page.locator('.form__submit')
    expect(btn_submit).to_be_visible()
    btn_submit.click()
    expect(page).to_have_url('http://frontend.niffler.dc/main')


def test_invalid_username_auth(page):
    invalid_username = 'Invalid username'
    invalid_password = '12345678'
    page.goto('http://auth.niffler.dc:9000/login')
    form_username = page.get_by_placeholder('Type your username')
    form_password = page.get_by_placeholder('Type your password')

    expect(form_password).to_be_visible()
    expect(form_username).to_be_visible()

    form_username.fill(invalid_username)
    form_password.fill(invalid_password)

    btn_submit = page.locator('.form__submit')

    expect(btn_submit).to_be_visible()

    btn_submit.click()
    msg_error = page.locator('.form__error')
    expect(msg_error).to_be_visible()


def test_invalid_password_auth(page, app_user):
    username, password = app_user
    invalid_password = '12345678'

    page.goto('http://auth.niffler.dc:9000/login')
    form_username = page.get_by_placeholder('Type your username')
    form_password = page.get_by_placeholder('Type your password')

    expect(form_password).to_be_visible()
    expect(form_username).to_be_visible()

    form_username.fill(username)
    form_password.fill(invalid_password)

    btn_submit = page.locator('.form__submit')

    expect(btn_submit).to_be_visible()

    btn_submit.click()
    msg_error = page.locator('.form__error')
    expect(msg_error).to_be_visible()


def test_no_values_auth(page):
    page.goto('http://auth.niffler.dc:9000/login')

    form_username = page.get_by_placeholder('Type your username')
    form_password = page.get_by_placeholder('Type your password')

    expect(form_password).to_be_visible()
    expect(form_username).to_be_visible()

    btn_submit = page.locator('.form__submit')

    expect(btn_submit).to_be_visible()

    btn_submit.click()


@Pages.main_page
def test_logout(page):
    page.locator('[aria-label="Menu"]').click()
    page.get_by_role("menuitem", name="Sign out").click()
    page.get_by_role('button', name="Log out").click()
    expect(page).to_have_url('http://auth.niffler.dc:9000/login')
    pass
