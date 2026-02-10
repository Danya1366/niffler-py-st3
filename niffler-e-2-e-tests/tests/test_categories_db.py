from playwright.sync_api import expect
from marks import Pages, TestData

TEST_CATEGORY_DB = "test_category_db"


@TestData.category(TEST_CATEGORY_DB)
def test_add_category_and_check_db(envs, category, spend_db):
    user_categories = spend_db.get_user_categories(envs.test_username)
    user_category_names = [category.name for category in user_categories]

    assert len(user_categories) > 0, "Категорий у этого пользовтаеля нет"
    assert category in user_category_names
