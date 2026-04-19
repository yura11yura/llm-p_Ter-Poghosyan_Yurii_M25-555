from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.users import UsersRepository
from app.repositories.chat_messages import ChatMessagesRepository
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.services.openrouter_client import OpenRouterClient
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_users_repo(db: AsyncSession = Depends(get_db)) -> UsersRepository:
    return UsersRepository(db)


async def get_messages_repo(db: AsyncSession = Depends(get_db)) -> ChatMessagesRepository:
    return ChatMessagesRepository(db)


def get_llm_client() -> OpenRouterClient:
    return OpenRouterClient()


async def get_auth_usecase(
    users_repo: UsersRepository = Depends(get_users_repo)
) -> AuthUseCase:
    return AuthUseCase(users_repo)


async def get_chat_usecase(
    messages_repo: ChatMessagesRepository = Depends(get_messages_repo),
    llm_client: OpenRouterClient = Depends(get_llm_client)
) -> ChatUseCase:
    return ChatUseCase(messages_repo, llm_client)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    users_repo: UsersRepository = Depends(get_users_repo)
) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id_str: Optional[str] = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ExpiredSignatureError, ValueError):
        raise credentials_exception
    
    user = await users_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user_id