from time import sleep

from click import pause
from playwright.sync_api import expect

from marks import Pages
from pages.profile_page import ProfilePage
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("ru_RU")
fake_category = fake.word()
count = 100
category_name = "new category"
description = "вчерашние траты"

@Pages.spending_page
def test_new_spending(page):

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
    page.get_by_role("gridcell", name=str(yesterday_day), exact=True).click()

    # Добавляем описание трате
    description_input = page.locator('input[name="description"]')

    description_input.click()

    description_input.fill(f'{description}')

    # Сохраняем трату
    add_btn = page.locator('#save')

    add_btn.click()

    # проверяем переход на мейн страницу
    expect(page).to_have_url('http://frontend.niffler.dc/main')