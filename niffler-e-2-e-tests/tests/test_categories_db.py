from marks import TestData
from test_data import TestConstants


@TestData.category(TestConstants.TEST_CATEGORY_BD)
def test_add_category_and_check_db(envs, category, spend_db):
    user_categories = spend_db.get_user_categories(envs.test_username)
    user_category_names = [category.name for category in user_categories]

    assert len(user_categories) > 0, "Категорий у этого пользовтаеля нет"
    assert category in user_category_names


def test_delete_category_and_check_db(envs, spend_db):
    new_category = spend_db.add_user_category(envs.test_username, TestConstants.TEST_CATEGORY_BD)

    search_before_delete = spend_db.get_category_by_id(new_category.id)
    assert search_before_delete.name == TestConstants.TEST_CATEGORY_BD

    spend_db.delete_category(new_category.id)

    search_after_delete = spend_db.get_category_by_name(envs.test_username, new_category.name)
    assert search_after_delete is None
