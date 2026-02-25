from faker import Faker

from marks import Pages
from test_data import UserCreds

fake = Faker("ru_RU")


@Pages.open_profile_page
def test_user_profile(envs, profile_page):
    profile_page.expect_profile_data(envs.test_username)


@Pages.open_profile_page
def test_add_name(profile_page):
    profile_page.add_name_in_profile(UserCreds.name)


@Pages.open_profile_page
def test_delete_added_name(profile_page):
    profile_page.add_name_in_profile(UserCreds.name)
    profile_page.delete_added_profile_name()


@Pages.open_profile_page
def test_edit_added_name(profile_page):
    profile_page.add_name_in_profile(UserCreds.name)
    profile_page.delete_profile_name()
    profile_page.add_name_in_profile(UserCreds.edited_name)


@Pages.open_profile_page
def test_add_new_category(profile_page):
    category_name = fake.word()

    profile_page.add_new_category(category_name)


@Pages.open_profile_page
def test_archive_category(profile_page):
    category_name = fake.word()

    profile_page.add_new_category(category_name)
    profile_page.archive_category(category_name)
