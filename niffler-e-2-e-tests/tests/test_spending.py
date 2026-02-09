from playwright.sync_api import expect

from conftest import main_page
from marks import Pages, TestData
from faker import Faker

from pages.spending_page import SpendingPage
from pages.main_page import MainPage
from models.spend import SpendAdd, CategoryAdd

fake = Faker("ru_RU")
fake_category = fake.word()
amount_to_add = 100
category_name = "new category"
description = "вчерашние траты"


@Pages.spending_page
def test_new_spending(page, spends_client, spend_db):
    spending_page = SpendingPage(page)
    expect(page).to_have_url('http://frontend.niffler.dc/spending')
    spending_page.add_amount(amount_to_add)
    spending_page.add_category(category_name)
    spending_page.set_the_date_to_yesterday()
    spending_page.add_description(description)
    add_btn = page.locator('#save')
    add_btn.click()
    expect(page).to_have_url('http://frontend.niffler.dc/main')
    main_page = MainPage(page)
    main_page.remove_all_spends()


TEST_CATEGORY_1 = "категория 1"
TEST_CATEGORY_2 = "Категория 2"
edited_amount = 200.03
edited_description = 'Тест'


@TestData.category(TEST_CATEGORY_1)
@TestData.spends({
    "amount": 101.1,
    "description": "test_description",
    "category": {
        "name": TEST_CATEGORY_1
    },
    "spendDate": "2025-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_update_spending(page, category, spends, envs):
    page.goto(envs.frontend_url)
    expect(page.locator('[aria-labelledby="tableTitle"]')).to_be_visible()
    expect(page.locator('[aria-labelledby="tableTitle"]')).to_contain_text('test_description')
    page.get_by_role("checkbox", name=TEST_CATEGORY_1).get_by_label("Edit spending").click()
    spending_page = SpendingPage(page)
    spending_page.amount_input_field.click()
    spending_page.amount_input_field.press("ControlOrMeta+A")
    spending_page.amount_input_field.press('Backspace')
    spending_page.amount_input_field.fill(str(edited_amount))
    spending_page.category_input_field.click()
    spending_page.category_input_field.fill(TEST_CATEGORY_1)
    spending_page.add_description(edited_description)
    spending_page.btn_save.click()
    expect(page).to_have_url('http://frontend.niffler.dc/main')
    statistics_icon = page.locator('[id="stat"]')
    expect(statistics_icon).to_contain_text(f"{TEST_CATEGORY_1} {edited_amount} ₽")
    expect(page.locator('[aria-labelledby="tableTitle"]')).to_contain_text(edited_description)
    expect(page.locator('[aria-labelledby="tableTitle"]')).to_contain_text(str(edited_amount))
    expect(page.locator('[aria-labelledby="tableTitle"]')).to_contain_text(TEST_CATEGORY_1)


@Pages.main_page
@TestData.category(TEST_CATEGORY_1)
@TestData.spends({
    "amount": "108.51",
    "description": "QA>GURU Python Advanced 6",
    "category": {
        "name": TEST_CATEGORY_1
    },
    "spendDate": "2024-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_delete_all_spendings(page, category, spends, spends_client, spend_db):
    category = spends_client.add_category(CategoryAdd(name="QA_GURU"))
    spends_client.add_spends({
        "amount": 200.01,
        "description": "Second Product",
        "category": {"name": "QA_GURU"},
        "spendDate": "2024-08-08T18:39:27.955Z",
        "currency": "RUB"
    })
    page.reload()
    container_history_of_spending = page.locator('[id="spendings"]')
    expect(container_history_of_spending).to_be_visible()
    main_page = MainPage(page)
    main_page.remove_all_spends()
    expect(container_history_of_spending).to_contain_text('There are no spendings')
    spend_db.delete_category(category.id)


amount2 = 99.99
amount1 = 108.51


@Pages.main_page
@TestData.category(TEST_CATEGORY_1)
@TestData.spends({
    "amount": amount1,
    "description": "QA>GURU Python Advanced 6",
    "category": {
        "name": TEST_CATEGORY_1
    },
    "spendDate": "2024-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_total_of_spend(page, category, spends):
    page.reload()
    main_page = MainPage(page)
    main_page.add_new_spend_btn.click()
    spending_page = SpendingPage(page)
    spending_page.add_amount(str(amount2))
    spending_page.add_category(TEST_CATEGORY_1)
    spending_page.add_description('eddited category')
    spending_page.save_change()
    main_page = MainPage(page)
    total_amount = float(amount1) + float(amount2)
    expected_text = f"{TEST_CATEGORY_1} {total_amount} ₽"
    expect(main_page.statistics_container).to_contain_text(expected_text)
    main_page.remove_all_spends()
