from app.repositories.users import UsersRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.schemas.user import UserPublic


class AuthUseCase:
    """Класс сценариев аутентификации и управления профилем пользователя."""
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo

    async def register(self, email: str, password: str) -> UserPublic:
        """
        Регистрирует нового пользователя в системе.
        
        Аргументы:
            email - email нового пользователя
            password - пароль в открытом виде
            
        Возвращает:
            UserPublic - публичные данные созданного пользователя
        """
        existing = await self.users_repo.get_by_email(email)
        if existing:
            raise ConflictError("User with this email already exists.")
        
        hashed = hash_password(password)
        user = await self.users_repo.create(email, hashed)
        return UserPublic.model_validate(user)
    
    async def login(self, email: str, password: str) -> str:
        """
        Аутентифицирует пользователя и выдаёт JWT токен.
        
        Аргументы:
            email - email пользователя
            password - пароль в открытом виде
            
        Возвращает:
            JWT access token
        """
        user = await self.users_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password.")

        return create_access_token(subject=str(user.id), role=user.role)
    
    async def get_profile(self, user_id: int) -> UserPublic:
        """
        Получает профиль пользователя по ID.
        
        Аргументы:
            user_id - id пользователя

        Возвращает:
            UserPublic - данные пользователя
        """
        user = await self.users_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found.")
        return UserPublic.model_validate(user)
