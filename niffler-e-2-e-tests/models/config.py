from pydantic import BaseModel


class Envs(BaseModel):
    frontend_url: str
    gateway_url: str
    auth_url: str
    register_url: str
    profile_url: str
    spending_url: str
    main_page_url: str
    login_url:str
    spend_db_url: str
    test_username: str
    test_password: str