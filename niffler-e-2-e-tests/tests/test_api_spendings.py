import pytest
import requests
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
def test_spending_should_be_deleted(page, category, spends, main_page):
    page.reload()
    main_page.expect_content_of_table("QA>GURU Python Advanced 6")
    main_page.delete_spend(TEST_CATEGORY)
    main_page.expect_content_of_table_is_empty("QA>GURU Python Advanced 6")
