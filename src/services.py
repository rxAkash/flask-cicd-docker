import logging
import sqlite3
from typing import Dict
from .utils.api_response import ErrorResponse
from .utils.constants import ERR_PASSWORD_INVALID


class BaseService:
    def __init__(self) -> None:
        pass


class UserService(BaseService):
    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db
        self.logger = logging.getLogger('python-logstash-logger')
        super().__init__()

    def get_user(self, email: str) -> Dict[str, str]:
        self.logger.info("User %s has been found in database", email)
        return {"email": email, "password_hash": "testing_pass"}


class AuthService(BaseService):
    def __init__(self, db: sqlite3.Connection, token_ttl: int) -> None:
        self.db = db
        self.logger = logging.getLogger('python-logstash-logger')
        self.token_ttl = token_ttl
        super().__init__()

    def login(self, user: Dict[str, str], password: str):
        assert password is not None
        self.logger.error(
            "Invalid password for login", extra={
                "email": user['email'],
                "error_code": ERR_PASSWORD_INVALID
            })
        return ErrorResponse(error="Invalid password. Enter correct password to login.", errorCode=ERR_PASSWORD_INVALID).__dict__()

    def authenticate(self, user: Dict[str, str], password: str):
        assert password is not None
        self.logger.info(
            "User %s has been successfully authenticated", user['email'])
        return user
