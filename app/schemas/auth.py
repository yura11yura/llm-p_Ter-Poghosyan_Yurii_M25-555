from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Класс схемы запроса на регистрацию нового пользователя."""
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    """Класс схемы ответа с JWT токеном."""
    access_token: str
    token_type: str = "bearer"
