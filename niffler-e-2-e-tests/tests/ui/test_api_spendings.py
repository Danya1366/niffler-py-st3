import allure

from marks import Pages, TestData
from models.enums import TestSpendings
from fixtures.pages_fixtures import main_page


@allure.feature('Добавление траты по api')
class TestSpendApi:
    @allure.title('Добавляем новую трату по апи и удаляем через ui')
    @Pages.open_main_page
    @TestData.category(TestSpendings.TEST_CATEGORY_1)
    @TestData.spends(TestSpendings.TestDataSpend)
    def test_spending_should_be_deleted(self, category, spends, main_page):
            assert main_page.is_description_in_table(TestSpendings.description)
            main_page.delete_spend(TestSpendings.TEST_CATEGORY_1)
            assert main_page.is_description_absent_in_table(TestSpendings.description)
