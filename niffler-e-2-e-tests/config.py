class TestUsers:
    """Тестовые пользователи"""
    USER_1 = {
        "username": "Test User 2",
        "password": "123321"
    }
    USER_2 = {
        "username": "Test User 5",
        "password": "123321"
    }
    INVALID_USER = {
        "username": "InvalidUser",
        "password": "wrongpass"
    }

class URLs:
    """Тестовые урлы"""
    auth_URl = "http://auth.niffler.dc:9000"
    base_URL = "http://frontend.niffler.dc"
    login = "/login"
    register = "/register"
    main = "/main"