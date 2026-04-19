from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    """Класс схемы пользователя для ответов API."""
    id: int
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)