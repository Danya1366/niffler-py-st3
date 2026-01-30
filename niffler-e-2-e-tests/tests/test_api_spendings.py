import pytest
import requests
from marks import Pages, TestData
from playwright.sync_api import Page,expect


@Pages.main_page
def test_spending_title_exists(page):
    expect(page).to_have_url('http://frontend.niffler.dc/')
    expect(page.get_by_text("History of Spendings")).to_be_visible()


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



def test_spending_should_deleted(page, category, spends):
    page.reload()
    expect(page.locator('[aria-labelledby="tableTitle"]')).to_be_visible()
    expect(page.locator('[aria-labelledby="tableTitle"]')).to_contain_text('QA>GURU Python Advanced 6')
    page.get_by_role("checkbox", name="school", exact=True).uncheck()
    page.get_by_role("checkbox", name="school", exact=True).check()
    page.locator("#delete").click()
    page.get_by_role("button", name="Delete").click()
    container_history_of_spending = page.locator('[id="spendings"]')
    expect(container_history_of_spending).not_to_contain_text('QA>GURU Python Advanced 6')









