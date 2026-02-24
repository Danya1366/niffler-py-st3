from marks import Pages, TestData
from test_data import TestSpendings


@Pages.main_page
@TestData.category(TestSpendings.TEST_CATEGORY_1)
@TestData.spends(TestSpendings.TestDataSpend)
def test_spending_should_be_deleted(page, category, spends, main_page):
    page.reload()
    main_page.expect_content_of_table("QA>GURU Python Advanced 6")
    main_page.delete_spend(TestSpendings.TEST_CATEGORY_1)
    main_page.expect_content_of_table_is_empty("QA>GURU Python Advanced 6")
