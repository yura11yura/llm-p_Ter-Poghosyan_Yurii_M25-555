from typing import List, Dict, Optional

from app.repositories.chat_messages import ChatMessagesRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    """Класс сценариев работы с LLM."""
    def __init__(
        self,
        messages_repo: ChatMessagesRepository,
        llm_client: OpenRouterClient
    ):
        self.messages_repo = messages_repo
        self.llm_client = llm_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: Optional[str] = None,
        max_history: int = 12,
        temperature: float = 0.7
    ) -> str:
        """
        Отправляет запрос к LLM с учетом истории диалога.
        
        Аргументы:
            user_id - id пользователя, отправившего запрос
            prompt - текст запроса
            system - системная инструкция для модели
            max_history - максимальное количество сообщений из истории
            temperature - температура генерации
            
        Возвращает:
            Текст ответа от языковой модели
        """
        llm_messages: List[Dict[str, str]] = []

        if system:
            llm_messages.append({"role": "system", "content": system})

        history = await self.messages_repo.get_recent_messages(user_id, max_history)
        for message in history:
            llm_messages.append({"role": message.role, "content": message.content})
        

        llm_messages.append({"role": "user", "content": prompt})

        await self.messages_repo.add_message(user_id, "user", prompt)

        answer = await self.llm_client.chat_completion(llm_messages, temperature)

        await self.messages_repo.add_message(user_id, "assistant", answer)

        return answer
    
    async def get_history(self, user_id: int, limit: int = 50) -> List[Dict]:
        """
        Получает историю диалога пользователя.
        
        Аргументы:
            user_id - id пользователя
            limit - максимальное количество возвращаемых сообщений
            
        Возвращает:
            Список сообщений с полями role, content, created_at
        """
        messages = await self.messages_repo.get_recent_messages(user_id, limit)
        return [
            {"role": message.role, "content": message.content, "created_at": message.created_at}
            for message in messages
        ]
    
    async def clear_history(self, user_id: int) -> None:
        """Удаляет всю историю диалога пользователя."""
        await self.messages_repo.delete_all_for_user(user_id)