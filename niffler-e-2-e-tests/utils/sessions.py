from urllib.parse import parse_qs, urlparse

import requests
from requests import Session


def allure_attach_request(function):
    """Декоратор логирования запроса и ответа в allure шаг и allure аттачмент"""
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise
        return response

    return wrapper


class BaseSession(Session):
    """Сессия с прокидыванием base_url и логированием запроса, ответа, хедеров ответа."""
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.base_url = kwargs.pop("base_url", "")

    @allure_attach_request
    def request(self, method, url, **kwargs):
        """Логирование запроса и вклейка base_url."""
        return super().request(method, self.base_url + url, **kwargs)


class AuthSession(Session):
    """Сессия с прокидыванием base_url и логированием запроса, ответа, хедеров ответа.
    + Автосохранение cookies внутри сессии из каждого response и redirect response, и 'code'."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.base_url = kwargs.pop("base_url", "")
        self.code = None

    @allure_attach_request
    def request(self, method, url, **kwargs):
        """Сохраняем все куки из редиректа и сохраняем code авторизации из redirect_uri
        и используем в дальнейшем в последующих запросах этой сессии"""
        response = super().request(method, self.base_url + url, **kwargs)
        for r in response.history:
            cookies = r.cookies.get_dict()
            self.cookies.update(cookies)
            code = parse_qs(urlparse(r.headers.get("Location")).query).get("code", None)
            if code:
                self.code = code
            return response.json()
