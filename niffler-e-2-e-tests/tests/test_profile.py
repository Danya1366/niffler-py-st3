from playwright.sync_api import expect
from faker import Faker
from marks import Pages

fake = Faker("ru_RU")
fake_category = fake.word()

username  = 'Test User 5'

@Pages.main_page
def test_user_profile(page, app_user):
    username, password = app_user
    user_icon = page.locator('[data-testid="PersonIcon"]')
    expect(user_icon).to_be_visible()
    user_icon.click()
    profile_btn = page.locator('a[href="/profile"]')
    expect(profile_btn).to_be_visible()
    profile_btn.click()
    username_input = page.locator("//*[@id='username']")
    expect(username_input).to_be_visible()
    expect(username_input).to_have_value(username)
    expect(page)

@Pages.profile_page
def test_add_name(page):

    name_input = page.locator('[name="name"]')
    expect(name_input).to_be_visible()

    name_input.click()
    name_input.fill('Тестовый пользователь')

    submit_btn = page.get_by_text('Save changes')
    submit_btn.click()

    success_alert = page.get_by_test_id("SuccessOutlinedIcon")
    expect(success_alert).to_be_visible()

@Pages.profile_page
def test_delete_added_name(page):

    name_input = page.locator('[name="name"]')
    expect(name_input).to_be_visible()

    name_input.click()
    name_input.fill('Тестовый пользователь')

    submit_btn = page.get_by_text('Save changes')
    submit_btn.click()

    success_alert = page.get_by_test_id("SuccessOutlinedIcon")
    expect(success_alert).to_be_visible()

    name_input.click(click_count=3)
    name_input.press('Delete')

    expect(name_input).to_have_value('')
    submit_btn.click()
    expect(success_alert).to_be_visible()

    page.reload()

    expect(name_input).to_have_value('')



@Pages.profile_page
def test_add_new_category(page):

    category_input = page.locator('[name="category"]')
    category_input.fill(fake_category)
    category_input.press("Enter")

    alert_added_new_category = page.get_by_role("alert")
    expect(alert_added_new_category).to_contain_text(f"You've added new category: {fake_category}")

    category_block = page.locator("div.MuiGrid-item", has=page.get_by_text(fake_category))

    expect(category_block).to_be_visible()

@Pages.profile_page
def test_archive_category(page):

    category_input = page.locator('[name="category"]')
    category_input.fill(fake_category)
    category_input.press("Enter")

    category_block = page.locator("div.MuiGrid-item", has=page.get_by_text(fake_category))

    archive_button = category_block.get_by_label("Archive category")
    archive_button.click()

    btn_archive = page.get_by_role('button', name = "Archive")

    btn_archive.click()

    expect(category_block).not_to_be_visible()

    archive_checkbox = page.get_by_role("checkbox", name = "Show archived")

    archive_checkbox.click()

    expect(category_block).to_be_visible()
