import jwt
import logging
from passlib.context import CryptContext
from datetime import datetime, timedelta
from application.exceptions.exp_service import (
    InvalidAccessToken,
    ExpiredAccessToken,
    InvalidRefreshToken,
    InvalidScopeToken,
    ExpiredRefreshToken,
)
from application.interfaces.services.auth import IAuthService

from src.config import settings

logger = logging.getLogger(__name__)


class AuthService(IAuthService):
    """Сервис для работы с аутентификацией и авторизацией."""

    hasher = CryptContext(schemes=['bcrypt'])
    secret = settings().SECRET_KEY
    algoritm = settings().ALGORITHM

    def encode_password(self, password: str) -> str:
        logger.info(
            'msg details: успешное завершение [%s]\n'
            'service func: %s.' % (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                                  self.encode_password.__name__))
        return self.hasher.hash(password)

    def verify_password(self, password: str, encoded_password: str) -> bool:
        logger.info(
            'msg details: успешное завершение [%s]\n'
            'service func: %s.' % (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                                  self.verify_password.__name__))
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, username: str) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': username
        }
        logger.info(
            'msg details: успешное завершение [%s]\n'
            'service func: %s.' % (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                                  self.encode_token.__name__))
        return jwt.encode(
            payload,
            self.secret,
            algorithm=self.algoritm
        )

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algoritm])
            if (payload['scope'] == 'access_token'):
                logger.info(
                    'msg details: успешное завершение [%s]\n'
                    'service func: %s.' % (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                                          self.decode_token.__name__))
                return payload['sub']
            raise InvalidScopeToken("Неверная область действия токена")
        except jwt.ExpiredSignatureError as e:
            logger.error(
                'msg details: %s [%s]\n'
                'service func: %s.\nОшибка: Истек срок действия токена доступа' %
                (e, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                 self.refresh_token.__name__))
            raise ExpiredAccessToken("Истек срок действия токена доступа")
        except jwt.InvalidTokenError as e:
            logger.error(
                'msg details: %s [%s]\n'
                'service func: %s.\nОшибка: Неверный токен доступа' %
                (e, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                 self.refresh_token.__name__))
            raise InvalidAccessToken("Неверный токен доступа")

    def encode_refresh_token(self, username: str) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, hours=10),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': username
        }
        logger.info(
            'msg details: успешное завершение [%s]\n'
            'service func: %s.' % (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                                  self.encode_refresh_token.__name__))
        return jwt.encode(
            payload,
            self.secret,
            algorithm=self.algoritm
        )

    def refresh_token(self, refresh_token: str) -> str:
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=[self.algoritm])
            if (payload['scope'] == 'refresh_token'):
                username = payload['sub']
                new_token = self.encode_token(username)
                logger.info(
                    'msg details: успешное завершение [%s]\n'
                    'service func: %s.' % (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                                          self.refresh_token.__name__))
                return new_token
            raise InvalidScopeToken("Неверная область действия токена")
        except jwt.ExpiredSignatureError as e:
            logger.error(
                'msg details: %s [%s]\n'
                'service func: %s.\nОшибка: Истек срок действия токена обновления' %
                (e, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                 self.refresh_token.__name__))
            raise ExpiredRefreshToken("Истек срок действия токена обновления")
        except jwt.InvalidTokenError as e:
            logger.error(
                'msg details: %s [%s]\n'
                'service func: %s.\nОшибка: Неверный токен обновления' %
                (e, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                 self.refresh_token.__name__))
            raise InvalidRefreshToken("Неверный токен обновления")
