import pkce
from models.config import Envs
from models.oauth import OAuthRequest
from utils.sessions import AuthSession


class OAuthClient:
    """Авторизуемся по Oauth2.0"""

    base_url: str

    def __init__(self, env: Envs):
        """Генерируем code_verifier и code_challenge. И гененрируем basic auth token из секрета сервиса авторизации"""
        self.session = AuthSession(base_url=env.auth_url)
        self.redirect_uri = env.frontend_url + "/authorized"
        self.code_verifier, self.code_challenge = pkce.generate_pkce_pair()

    def get_token(self, username, password):
        """Возвращает token oauth для авторизации пользователя с юзернейм
        1. Получем jsession и xsrf-token куку в сессию
        2. Получаем code из redirec по xsrf-token у
        3. Получаем access_token"""

        self.session.get(
            url="oauth2/authorize",
            params=OAuthRequest(
                redirect_uri=self.redirect_uri,
                code=self.session.code
            ).model_dump(),
            allow_redirects=True
        )
