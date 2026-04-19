from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UsersRepository:
    """Класс репозитория для работы с пользователями в базе данных."""
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Находит пользователя по email.
        
        Аргументы:
            email - email пользователя
        """
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Находит пользователя по ID.
        
        Аргументы:
            user_id - идентификатор пользователя
        """
        return await self._session.get(User, user_id)

    async def create(self, email: str, password_hash: str, role: str = "user") -> User:
        """
        Создаёт нового пользователя в базе данных.
        
        Аргументы:
            email - email нового пользователя
            password_hash - хеш пароля
            role - роль пользователя
            
        Возвращает:
            user - созданный пользователь
        """
        user = User(email=email, password_hash=password_hash, role=role)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
