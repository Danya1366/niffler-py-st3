import allure

from marks import TestData
from models.enums import Constants


@allure.feature('Категории')
class TestCategories:
    @allure.title('Добавление категорий и проверка базы данных')
    @TestData.category(Constants.TEST_CATEGORY_BD)
    def test_add_category_and_check_db(self, envs, category, spend_db):
        user_categories = spend_db.get_user_categories(envs.test_username)
        user_category_names = [category.name for category in user_categories]
        assert len(user_categories) > 0, "Категорий у этого пользовтаеля нет"
        assert category in user_category_names

    @allure.title('Удаление категории из базы данных')
    def test_delete_category_and_check_db(self, envs, spend_db):
        new_category = spend_db.add_user_category(
            envs.test_username,
            Constants.TEST_CATEGORY_BD
        )
        search_before_delete = spend_db.get_category_by_id(new_category.id)
        assert search_before_delete.name == Constants.TEST_CATEGORY_BD
        spend_db.delete_category(new_category.id)
        search_after_delete = spend_db.get_category_by_name(
            envs.test_username,
            new_category.name
        )
        assert search_after_delete is None
