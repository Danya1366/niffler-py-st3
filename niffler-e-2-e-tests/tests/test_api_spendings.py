from marks import Pages, TestData
from playwright.sync_api import expect

from pages.main_page import MainPage

TEST_CATEGORY = "school"


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": "108.51",
    "description": "QA>GURU Python Advanced 6",
    "category": {
        "name": TEST_CATEGORY
    },
    "spendDate": "2024-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_spending_should_be_deleted(page, category, spends):
    page.reload()
    main_page = MainPage(page)
    expect(main_page.expense_table).to_be_visible()
    expect(main_page.expense_table).to_contain_text('QA>GURU Python Advanced 6')
    main_page.delete_spend(TEST_CATEGORY)
    expect(main_page.container_history_of_spending).not_to_contain_text('QA>GURU Python Advanced 6')
