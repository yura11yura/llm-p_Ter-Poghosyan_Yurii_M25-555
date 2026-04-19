from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Хеширует пароль пользователя."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля хешу."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, role: str) -> str:
    """
    Создаёт JWT access token для аутентифицированного пользователя.

    Аргументы:
        subject - идентификатор пользователя
        role - роль пользователя

    Возвращает:
        JWT токен в виде строки
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": subject,
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def decode_token(token: str) -> Dict[str, Any]:
    """Декодирует JWT токен."""
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])