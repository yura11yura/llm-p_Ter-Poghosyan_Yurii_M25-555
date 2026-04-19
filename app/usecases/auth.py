from app.repositories.users import UsersRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.schemas.user import UserPublic


class AuthUseCase:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo

    async def register(self, email: str, password: str) -> UserPublic:
        existing = await self.users_repo.get_by_email(email)
        if existing:
            raise ConflictError("User with this email already exists.")
        
        hashed = hash_password(password)
        user = await self.users_repo.create(email, hashed)
        return UserPublic.model_validate(user)
    
    async def login(self, email: str, password: str) -> str:
        user = await self.users_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password.")

        return create_access_token(subject=str(user.id), role=user.role)
    
    async def get_profile(self, user_id: int) -> UserPublic:
        user = await self.users_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found.")
        return UserPublic.model_validate(user)
