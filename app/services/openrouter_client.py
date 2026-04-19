from app.core.config import settings
from app.core.errors import ExternalServiceError

from typing import List, Dict

import httpx

class OpenRouterClient:
    """Класс клиента для взаимодействия с OpenRouter API."""
    def __init__(self):
        self.base_url = settings.openrouter_base_url
        self.api_key = settings.openrouter_api_key
        self.model = settings.openrouter_model
        self.site_url = settings.openrouter_site_url
        self.app_name = settings.openrouter_app_name

    async def chat_completion(
        self, 
        messages: List[Dict[str, str]],
        temperature: float = 0.7
    ) -> str: 
        """
        Отправляет запрос к LLM и возвращает текст ответа.
        
        Аргументы:
            messages - список сообщений
            temperature - температура генерации
                
        Возвращает:
            Текст ответа от языковой модели
        """
        headers = {
            "Authorization": f"Beaver {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.app_name,
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature 
        }


        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers = headers,
                    json = payload
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                raise ExternalServiceError(
                    F"OpenRouter API error: {e.response.status_code} - {e.response.text}"
                )
            except Exception as e:
                raise ExternalServiceError(f"OpenRouter request failed: {str(e)}")

