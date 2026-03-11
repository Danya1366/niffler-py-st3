from urllib.parse import parse_qs, urlparse

import requests
from requests import Session


def raise_for_status(function):
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

    @raise_for_status
    def request(self, method, url, **kwargs):
        """Логирование запроса и вклейка base_url."""
        return super().request(method, self.base_url + url, **kwargs)


class AuthSession(BaseSession):
    """Сессия с прокидыванием base_url и логированием запроса, ответа, хедеров ответа.
    + Автосохранение cookies внутри сессии из каждого response и redirect response, и 'code'."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = None

    @raise_for_status
    def request(self, method, url, **kwargs):
        """Сохраняем все куки из редиректа и сохраняем code авторизации из redirect_uri
        и используем в дальнейшем в последующих запросах этой сессии"""
        response = super().request(method, url, **kwargs)
        for r in response.history:
            cookies = r.cookies.get_dict()
            self.cookies.update(cookies)
            code = parse_qs(urlparse(r.headers.get("Location")).query).get("code", None)
            if code:
                self.code = code
        return response
