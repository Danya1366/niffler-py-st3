import allure
import pytest

from marks import Pages, TestData
from models.enums import Constants, Spendings


@allure.feature('Траты')
@allure.story('API + UI')
@pytest.mark.xdist_group("group2")
class TestSpends:
    @allure.title('Добавление новой траты за вчерашний день')
    @Pages.open_spending_page
    def test_new_spending_with_yesterday_date(self, envs, spending_page, main_page, clean_spendings_setup):
        spending_page.add_new_spending_with_last_date(
            Constants.amount_to_add,
            Constants.category_to_add,
            Constants.description_to_add
        )
        spending_page.click_save_btn(envs)
        assert main_page.is_statistics_correct(
            Constants.category_to_add,
            Constants.amount_to_add
        )
        assert main_page.is_description_in_table(Constants.description_to_add)
        assert main_page.is_amount_in_table(Constants.amount_to_add)
        assert main_page.is_category_in_table(Constants.category_to_add)

    @allure.title('Обновление созданной траты')
    @Pages.open_main_page
    @TestData.spends(Spendings.TestDataSpend)
    def test_update_spending(self, spends, envs, spending_page, main_page):
        assert main_page.is_description_absent_in_table(Constants.description)
        main_page.click_on_checkbox_with_name(Constants.TEST_CATEGORY_1)
        spending_page.update_amount(Constants.edited_amount)
        spending_page.update_category(Constants.edited_category)
        spending_page.add_description(Constants.edited_description)
        spending_page.click_save_btn(envs)
        assert main_page.is_statistics_correct(
            Constants.edited_category,
            Constants.edited_amount
        )
        assert main_page.is_description_in_table(Constants.edited_description)
        assert main_page.is_amount_in_table(Constants.edited_amount)
        assert main_page.is_category_in_table(Constants.edited_category)

    @allure.title('Удаление всех трат')
    @Pages.open_spending_page
    @TestData.spends(Spendings.TestDataSpend)
    def test_delete_all_spendings(self, spends, spending_page, main_page, clean_spendings_setup):
        spending_page.add_new_spending(
            Constants.amount_for_delete,
            Constants.category_for_delete,
            Constants.description_for_delete
        )
        main_page.remove_all_spends()
        assert main_page.is_description_absent_in_table(Constants.description_for_delete)

    @allure.title('Сумма всех трат')
    @Pages.open_main_page
    def test_total_of_spend(self, spending_page, main_page, clean_spendings_setup):
        main_page.go_to_spend()
        spending_page.add_new_spending(
            Constants.amount1,
            Constants.TEST_CATEGORY_1,
            Constants.description
        )
        main_page.go_to_spend()
        spending_page.add_new_spending(
            Constants.amount2,
            Constants.TEST_CATEGORY_1,
            Constants.description
        )
        assert main_page.is_total_amount_correct(
            Constants.TEST_CATEGORY_1,
            Constants.amount1,
            Constants.amount2
        )


@allure.feature('Траты')
@allure.story('API + UI')
@pytest.mark.xdist_group("group2")
class TestSpendApi:
    @allure.title('Добавляем новую трату по апи и удаляем через ui')
    @Pages.open_main_page
    @TestData.category(Spendings.TEST_CATEGORY_2)
    @TestData.spends(Spendings.TestDataSpend_1)
    def test_spending_should_be_deleted(self, category, spends, main_page):
        assert main_page.is_description_in_table(Spendings.description)
        main_page.delete_spend(Spendings.TEST_CATEGORY_2)
        assert main_page.is_description_absent_in_table(Spendings.description)
