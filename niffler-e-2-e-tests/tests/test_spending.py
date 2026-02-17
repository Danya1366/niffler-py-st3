from playwright.sync_api import expect

from conftest import main_page
from marks import Pages, TestData
from faker import Faker

from pages.main_page import MainPage

TEST_CATEGORY_1 = "категория 1"


@Pages.open_spending_page
def test_new_spending_with_yesterday_date(page, envs, spending_page):
    amount_to_add = "100"
    category_name = "new category"
    description = "вчерашние траты"

    spending_page.add_new_spending_with_last_date(amount_to_add, category_name, description)
    spending_page.btn_save.click()
    expect(page).to_have_url(envs.frontend_url + "/main")
    main_page = MainPage(page)
    main_page.expect_expense_table(amount_to_add, category_name, description)
    main_page.remove_all_spends()





@Pages.main_page
@TestData.spends({
    "amount": "108.51",
    "description": "QA>GURU Python Advanced 6",
    "category": {
        "name": "категория 1"
    },
    "spendDate": "2024-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_update_spending(page, spends, envs, spending_page):
    edited_amount = "200.03"
    edited_category = 'Тестовая для проверки изменений'
    edited_description = 'Тест'

    page.reload()

    main_page = MainPage(page)
    expect(main_page.expense_table).to_contain_text('QA>GURU Python Advanced 6')
    page.get_by_role("checkbox", name=TEST_CATEGORY_1).get_by_label("Edit spending").click()
    spending_page.update_amount(edited_amount)
    spending_page.update_category(edited_category)
    spending_page.add_description(edited_description)
    spending_page.btn_save.click()
    expect(page).to_have_url(envs.frontend_url + "/main")
    main_page.expect_expense_table(edited_amount, edited_category, edited_description)
    main_page.remove_all_spends()


@Pages.open_spending_page
@TestData.spends({
    "amount": "108.51",
    "description": "QA>GURU Python Advanced 6",
    "category": {
        "name": TEST_CATEGORY_1
    },
    "spendDate": "2024-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_delete_all_spendings(page, spends, spending_page):
    amount = "200.01"
    category = "QA_GURU"
    description = "Second Product"
    spending_page.add_new_spending(amount, category, description)
    main_page = MainPage(page)
    expect(main_page.container_history_of_spending).to_be_visible()
    main_page.remove_all_spends()


@Pages.main_page
@TestData.spends({
    "amount": "108.51",
    "description": "QA>GURU Python Advanced 6",
    "category": {
        "name": TEST_CATEGORY_1
    },
    "spendDate": "2024-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_total_of_spend(page, spends,envs, spending_page):
    description = 'eddited category'
    amount1 = "108.51"
    amount2 = "99.99"

    page.reload()
    main_page = MainPage(page)
    main_page.go_to_spend(envs.frontend_url)
    spending_page.add_new_spending(amount2, TEST_CATEGORY_1, description)
    total_amount = float(amount1) + float(amount2)
    expected_text = f"{TEST_CATEGORY_1} {total_amount} ₽"
    expect(main_page.statistics_container).to_contain_text(expected_text)
    main_page.remove_all_spends()
