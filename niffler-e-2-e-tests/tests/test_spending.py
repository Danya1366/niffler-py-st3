import allure

from marks import Pages, TestData
from models.enums import TestConstants, TestSpendings


@allure.feature('Траты')
class TestSpends:
    @allure.title('Добавление новой траты за вчерашний день')
    @Pages.open_spending_page
    def test_new_spending_with_yesterday_date(self, envs, spending_page, main_page, clean_spendings_setup):
        spending_page.add_new_spending_with_last_date(TestConstants.amount_to_add, TestConstants.category_to_add,
                                                      TestConstants.description_to_add)
        spending_page.click_save_btn(envs)
        assert main_page.is_statistics_correct(TestConstants.category_to_add, TestConstants.amount_to_add)
        assert main_page.is_description_in_table(TestConstants.description_to_add)
        assert main_page.is_amount_in_table(TestConstants.amount_to_add)
        assert main_page.is_category_in_table(TestConstants.category_to_add)

    @allure.title('Обновление созданной траты')
    @Pages.open_main_page
    @TestData.spends(TestSpendings.TestDataSpend)
    def test_update_spending(self, spends, envs, spending_page, main_page, clean_spendings_setup):
        assert main_page.is_description_absent_in_table(TestConstants.description)
        main_page.click_on_checkbox_with_name(TestConstants.TEST_CATEGORY_1)
        spending_page.update_amount(TestConstants.edited_amount)
        spending_page.update_category(TestConstants.edited_category)
        spending_page.add_description(TestConstants.edited_description)
        spending_page.click_save_btn(envs)
        assert main_page.is_statistics_correct(TestConstants.edited_category, TestConstants.edited_amount)
        assert main_page.is_description_in_table(TestConstants.edited_description)
        assert main_page.is_amount_in_table(TestConstants.edited_amount)
        assert main_page.is_category_in_table(TestConstants.edited_category)

    @allure.title('Удаление всех трат')
    @Pages.open_spending_page
    @TestData.spends(TestSpendings.TestDataSpend)
    def test_delete_all_spendings(self, spends, spending_page, main_page, clean_spendings_setup):
        spending_page.add_new_spending(TestConstants.amount_for_delete, TestConstants.category_for_delete,
                                       TestConstants.description_for_delete)
        assert main_page.is_statistics_correct(TestConstants.category_for_delete, TestConstants.amount_for_delete)
        assert main_page.is_description_in_table(TestConstants.description_for_delete)
        assert main_page.is_amount_in_table(TestConstants.amount_for_delete)
        assert main_page.is_category_in_table(TestConstants.category_for_delete)

    @allure.title('Сумма всех трат')
    @Pages.open_main_page
    @TestData.spends(TestSpendings.TestDataSpend)
    def test_total_of_spend(self, spends, envs, spending_page, main_page, clean_spendings_setup):
        main_page.go_to_spend()
        spending_page.add_new_spending(TestConstants.amount2, TestConstants.TEST_CATEGORY_1, TestConstants.description)
        assert main_page.is_total_amount_correct(TestConstants.TEST_CATEGORY_1, TestConstants.amount1,
                                                     TestConstants.amount2)
