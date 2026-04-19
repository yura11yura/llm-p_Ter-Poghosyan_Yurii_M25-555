from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase
from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Отправка запроса к LLM и получение ответа."""
    try:
        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=request.prompt,
            system=request.system,
            max_history=request.max_history,
            temperature=request.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=e.detail)


@router.get("/history")
async def get_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
    limit: int = 50,
):
    """Возвращает историю диалога текущего пользователя."""
    history = await chat_usecase.get_history(user_id, limit)
    return {"history": history}


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Очищает историю диалога текущего пользователя."""
    await chat_usecase.clear_history(user_id)