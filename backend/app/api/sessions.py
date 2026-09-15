from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession

from app.database.repositories import (
    create_session,
    get_session,
    list_sessions,
)
from app.database.session import get_db
from app.schemas.session import (
    SessionCreate,
    SessionResponse,
)


router = APIRouter(
    prefix="/api/sessions",
    tags=["sessions"],
)


@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_session(
    payload: SessionCreate,
    db: DBSession = Depends(get_db),
):
    return create_session(
        db=db,
        title=payload.title,
    )


@router.get(
    "",
    response_model=list[SessionResponse],
)
def get_all_sessions(
    db: DBSession = Depends(get_db),
):
    return list_sessions(db)


@router.get(
    "/{session_id}",
    response_model=SessionResponse,
)
def get_one_session(
    session_id: str,
    db: DBSession = Depends(get_db),
):
    session = get_session(
        db=db,
        session_id=session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    return session