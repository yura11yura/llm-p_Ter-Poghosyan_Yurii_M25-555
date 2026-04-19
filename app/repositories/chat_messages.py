from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.models import ChatMessage

from typing import List

class ChatMessagesRepository:
    """Класс репозитория для работы с сообщениями чата в базе данных."""
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """
        Добавляет новое сообщение в историю чата.
        
        Аргументы:
            user_id - id пользователя, которому принадлежит сообщение
            role - роль отправителя
            content - текст сообщения
            
        Возвращает:
            message - созданное сообщение с заполненными полями
        """
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message
    
    async def get_recent_messages(self, user_id: int, limit: int) -> List[ChatMessage]:
        """
        Получает последние N сообщений пользователя в хронологическом порядке.

        Аргументы:
            user_id - id пользователя
            limit - максимальное количество возвращаемых сообщений
            
        Возвращает:
            List[ChatMessage] - список сообщений от старых к новым
        """
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        messages = result.scalars().all()
        return list(reversed(messages))
    
    async def delete_all_for_user(self, user_id: int) -> None:
        """
        Удаляет всю историю сообщений пользователя.
        
        Аргументы:
            user_id - id пользователя, чью историю нужно очистить
        """
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()