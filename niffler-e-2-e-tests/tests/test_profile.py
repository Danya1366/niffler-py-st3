import allure
from faker import Faker

from marks import Pages
from test_data import UserCreds

fake = Faker("ru_RU")


@allure.feature('Профиль пользователя')
class TestProfile:
    @allure.title('Проверка данных пользователя')
    @Pages.open_profile_page
    def test_user_profile(self, envs, profile_page):
        profile_page.expect_profile_data(envs.test_username)

    @allure.story('Имя пользователя')
    @allure.title('Добавление имени для профиля пользователя')
    @Pages.open_profile_page
    def test_add_name(self, profile_page):
        profile_page.add_name_in_profile(UserCreds.name)

    @allure.story('Имя пользователя')
    @allure.title('Удаление имени профиля пользователя')
    @Pages.open_profile_page
    def test_delete_added_name(self, profile_page):
        profile_page.add_name_in_profile(UserCreds.name)
        profile_page.delete_added_profile_name()
        profile_page.expect_deleted_profile_name()

    @allure.story('Имя пользователя')
    @allure.title('Редактирование имени пользователя')
    @Pages.open_profile_page
    def test_edit_added_name(self, profile_page):
        profile_page.add_name_in_profile(UserCreds.name)
        profile_page.delete_profile_name()
        profile_page.add_name_in_profile(UserCreds.edited_name)

    @allure.story('Категории UI')
    @allure.title('Добавление категории')
    @Pages.open_profile_page
    def test_add_new_category(self, profile_page):
        category_name = fake.word()

        profile_page.add_new_category(category_name)
        profile_page.expect_added_category(category_name)

    @allure.story('Категории UI')
    @allure.title('Архивация категории')
    @Pages.open_profile_page
    def test_archive_category(self, profile_page):
        category_name = fake.word()

        profile_page.add_new_category(category_name)
        profile_page.expect_added_category(category_name)
        profile_page.archive_category(category_name)
        profile_page.expect_arсhive_category(category_name)
