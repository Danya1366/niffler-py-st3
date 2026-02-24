from conftest import main_page
from marks import Pages, TestData
from test_data import TestConstants, TestSpendings


@Pages.open_spending_page
def test_new_spending_with_yesterday_date(envs, spending_page, main_page):
    spending_page.add_new_spending_with_last_date(TestConstants.amount_to_add, TestConstants.category_to_add,
                                                  TestConstants.description_to_add)
    spending_page.click_save_btn(envs)
    main_page.expect_expense_table(TestConstants.amount_to_add, TestConstants.category_to_add,
                                   TestConstants.description_to_add)
    main_page.remove_all_spends()


@Pages.main_page
@TestData.spends(TestSpendings.TestDataSpend)
def test_update_spending(spends, envs, spending_page, main_page):
    main_page.expect_content_of_table(TestSpendings.description)
    main_page.click_on_checkbox_with_name(TestConstants.TEST_CATEGORY_1)
    spending_page.update_amount(TestConstants.edited_amount)
    spending_page.update_category(TestConstants.edited_category)
    spending_page.add_description(TestConstants.edited_description)
    spending_page.click_save_btn(envs)
    main_page.expect_expense_table(TestConstants.edited_amount, TestConstants.edited_category,
                                   TestConstants.edited_description)
    main_page.remove_all_spends()


@Pages.open_spending_page
@TestData.spends(TestSpendings.TestDataSpend)
def test_delete_all_spendings(spends, spending_page, main_page):
    spending_page.add_new_spending(TestConstants.amount_for_delete, TestConstants.category_for_delete,
                                   TestConstants.description_for_delete)
    main_page.expect_expense_table(TestConstants.amount_for_delete, TestConstants.category_for_delete,
                                   TestConstants.description_for_delete)
    main_page.remove_all_spends()


@Pages.main_page
@TestData.spends(TestSpendings.TestDataSpend)
def test_total_of_spend(page, spends, envs, spending_page, main_page):
    page.reload()
    main_page.go_to_spend()
    spending_page.add_new_spending(TestConstants.amount2, TestConstants.TEST_CATEGORY_1, TestConstants.description)
    main_page.expect_statics_container_for_total(TestConstants.TEST_CATEGORY_1, TestConstants.amount1,
                                                 TestConstants.amount2)
    main_page.remove_all_spends()
