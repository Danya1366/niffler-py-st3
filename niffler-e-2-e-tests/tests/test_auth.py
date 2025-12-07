from time import sleep

import pytest
from playwright.sync_api import Page,expect
from config import TestUsers, URLs

URL = "http://auth.niffler.dc:9000"
login = "/login"

username = 'Test User 5'


def test_page_title(page:Page):
    page.goto(URLs.auth_URl + URLs.login)
    expect(page.locator('.header')).to_contain_text("Log in")

def test_create_new_user(page):
    page.goto(URLs.auth_URl + URLs.login)
    form_register = page.locator('.form__register')
    expect(form_register).to_be_visible()
    expect(form_register).to_contain_text('Create new account')
    form_register.click()
    expect(page).to_have_url(URLs.auth_URl + URLs.register)

    input_form_password = page.locator('#password')
    input_form_username = page.locator('input[name="username"]')
    input_form_password_submit = page.locator('#passwordSubmit')

    expect(input_form_password).to_be_visible()
    expect(input_form_username).to_be_visible()
    expect(input_form_password_submit).to_be_visible()

    input_form_username.fill(TestUsers.USER_2['username'])
    input_form_password.fill(TestUsers.USER_2["password"])
    input_form_password_submit.fill(TestUsers.USER_2["password"])

    page.locator('.form__submit').click()

    btn_sgn_in = page.locator('.form_sign-in')

    expect(page.locator('.form__paragraph_success')).to_be_visible()
    expect(btn_sgn_in).to_be_visible()

    btn_sgn_in.click()

    expect(form_register).to_be_visible()


def test_valid_auth(page):
    page.goto("http://auth.niffler.dc:9000/login")

    form_username = page.get_by_placeholder('Type your username')
    form_password = page.get_by_placeholder('Type your password')

    expect(form_password).to_be_visible()
    expect(form_username).to_be_visible()

    form_username.fill(TestUsers.USER_2['username'])
    form_password.fill(TestUsers.USER_2['password'])

    btn_submit = page.locator('.form__submit')

    expect(btn_submit).to_be_visible()

    btn_submit.click()

    expect(page).to_have_url('http://frontend.niffler.dc/main')

    sleep(3)


def test_invalid_username_auth(page):
    page.goto(URLs.auth_URl + URLs.login)
    form_username = page.get_by_placeholder('Type your username')
    form_password = page.get_by_placeholder('Type your password')

    expect(form_password).to_be_visible()
    expect(form_username).to_be_visible()

    form_username.fill(TestUsers.INVALID_USER["username"])
    form_password.fill(TestUsers.INVALID_USER["password"])

    btn_submit = page.locator('.form__submit')

    expect(btn_submit).to_be_visible()

    btn_submit.click()
    msg_error = page.locator('.form__error')
    expect(msg_error).to_be_visible()

def test_invalid_password_auth(page):
    page.goto(URLs.auth_URl + URLs.login)
    form_username = page.get_by_placeholder('Type your username')
    form_password = page.get_by_placeholder('Type your password')

    expect(form_password).to_be_visible()
    expect(form_username).to_be_visible()

    form_username.fill(TestUsers.USER_2["username"])
    form_password.fill(TestUsers.INVALID_USER["password"])

    btn_submit = page.locator('.form__submit')

    expect(btn_submit).to_be_visible()

    btn_submit.click()
    msg_error = page.locator('.form__error')
    expect(msg_error).to_be_visible()

def test_no_values_auth(page):
    page.goto(URLs.auth_URl + URLs.login)
    form_username = page.get_by_placeholder('Type your username')
    form_password = page.get_by_placeholder('Type your password')

    expect(form_password).to_be_visible()
    expect(form_username).to_be_visible()

    btn_submit = page.locator('.form__submit')

    expect(btn_submit).to_be_visible()

    btn_submit.click()

