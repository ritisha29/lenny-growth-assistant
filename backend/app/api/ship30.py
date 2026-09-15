from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.agent.router import AgentRouter
from app.database.repositories import create_artifact, get_session
from app.database.session import get_db


router = APIRouter(
    prefix="/api/ship30",
    tags=["ship30"],
)

agent_router = AgentRouter()


class Ship30Request(BaseModel):
    session_id: str
    topic: str = Field(
        min_length=3,
        max_length=500,
    )
    source_url: str | None = None


class Ship30Response(BaseModel):
    artifact_id: str
    essay: str


@router.post("", response_model=Ship30Response)
async def generate_ship30(
    request: Ship30Request,
    db: Session = Depends(get_db),
):
    try:
        session = get_session(
            db=db,
            session_id=request.session_id,
        )

        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Session not found",
            )

        essay = await agent_router.generate_ship30(
            topic=request.topic,
            source_url=request.source_url,
        )

        artifact = create_artifact(
            db=db,
            session_id=request.session_id,
            artifact_type="markdown",
            content=essay,
        )

        return {
            "artifact_id": artifact.id,
            "essay": essay,
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate Ship 30 essay: {exc}",
        )