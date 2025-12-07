from time import sleep

from playwright.sync_api import expect
from pages.profile_page import ProfilePage
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("ru_RU")
fake_category = fake.word()

def test_new_spending(auth,page):

    count = 100
    category_name = "new category"
    description = "вчерашние траты"

    page = auth
    spending_link = page.locator('a[href="/spending"]')
    expect(spending_link).to_be_visible()

    spending_link.click()

    expect(page).to_have_url('http://frontend.niffler.dc/spending')
    amount_input = page.locator('input[name="amount"]')
    amount_input.click()
    amount_input.press('Backspace')
    amount_input.fill(f'{count}')

    category_input = page.locator('input[name="category"]')

    category_input.click()

    category_input.fill(f'{category_name}')

    # Выставляем дату за вчера
    calendar_icon = page.locator('img[alt="Calendar"]')
    calendar_icon.click()

    yesterday = datetime.now() - timedelta(days=1)
    yesterday_day = yesterday.day

    page.locator(f'text={yesterday_day}').first.click()

    # Добавляем описание трате
    description_input = page.locator('input[name="description"]')

    description_input.click()

    description_input.fill(f'{description}')

    # Сохраняем трату
    add_btn = page.locator('#save')

    add_btn.click()

    # проверяем переход на мейн страницу
    expect(page).to_have_url('http://frontend.niffler.dc/main')