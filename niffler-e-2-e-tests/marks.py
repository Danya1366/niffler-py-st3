import pytest
class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param["description"])


class Pages:
    main_page = pytest.mark.usefixtures("main_page")
    profile_page = pytest.mark.usefixtures("profile_page")
    spending_page = pytest.mark.usefixtures("spending_page")