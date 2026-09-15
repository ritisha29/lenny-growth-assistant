from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/api", tags=["chat"])

chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    try:
        response = await chat_service.answer(
            session_id=request.session_id,
            question=request.message,
            db=db,
        )
        return response

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))