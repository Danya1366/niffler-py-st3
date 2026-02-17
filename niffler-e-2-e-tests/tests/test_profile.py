from playwright.sync_api import expect
from faker import Faker

from marks import Pages
from pages.profile_page import ProfilePage

fake = Faker("ru_RU")


@Pages.open_profile_page
def test_user_profile(envs, profile_page):
    expect(profile_page.username_input).to_be_visible()
    expect(profile_page.username_input).to_have_value(envs.test_username)


@Pages.open_profile_page
def test_add_name(page):
    name = "test user"

    profile_page = ProfilePage(page)
    profile_page.input_user_name(name)
    profile_page.save_changes_btn.click()
    expect(profile_page.success_alert).to_be_visible()


@Pages.open_profile_page
def test_delete_added_name(page):
    name = "test user"

    profile_page = ProfilePage(page)
    profile_page.input_user_name(name)
    profile_page.save_changes_btn.click()
    expect(profile_page.success_alert).to_be_visible()
    profile_page.delete_profile_name()
    page.reload()
    expect(profile_page.name_input).to_have_value('')


@Pages.open_profile_page
def test_edit_added_name(page):
    name = "test user"
    edited_name = "edited username"

    profile_page = ProfilePage(page)
    profile_page.input_user_name(name)
    profile_page.save_changes_btn.click()
    expect(profile_page.success_alert).to_be_visible()
    profile_page.delete_profile_name()
    profile_page.input_user_name(edited_name)
    profile_page.save_changes_btn.click()
    expect(profile_page.name_input).to_have_value(edited_name)


@Pages.open_profile_page
def test_add_new_category(page):
    category_name = fake.word()

    profile_page = ProfilePage(page)
    profile_page.add_new_category(category_name)
    expect(profile_page.get_category_block_by_name(category_name)).to_be_visible()


@Pages.open_profile_page
def test_archive_category(page):
    category_name = fake.word()

    profile_page = ProfilePage(page)
    profile_page.add_new_category(category_name)
    archive_button = profile_page.get_category_block_by_name(category_name).get_by_label("Archive category")
    archive_button.click()
    profile_page.btn_archive.click()
    expect(profile_page.get_category_block_by_name(category_name)).not_to_be_visible()
    profile_page.archive_checkbox.click()
    expect(profile_page.get_category_block_by_name(category_name)).to_be_visible()
