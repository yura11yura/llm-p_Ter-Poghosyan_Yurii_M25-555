from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)
):
    """Регистрация нового пользователя."""
    try:
        return await auth_usecase.register(payload.email, payload.password)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)
):
    """Вход в систему и получение JWT токена."""
    try:
        access_token = await auth_usecase.login(form_data.username, form_data.password)
        return TokenResponse(access_token=access_token)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@router.get("/me", response_model=UserPublic)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)
):
    """Возвращает профиля текущего пользователя."""
    try:
        return await auth_usecase.get_profile(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
