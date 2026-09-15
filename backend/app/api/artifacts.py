from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Artifact


router = APIRouter(
    prefix="/api/artifacts",
    tags=["artifacts"],
)


class ArtifactResponse(BaseModel):
    id: str
    session_id: str
    artifact_type: str
    content: str

    model_config = {
        "from_attributes": True,
    }


@router.get("/{artifact_id}", response_model=ArtifactResponse)
def get_artifact(
    artifact_id: str,
    db: Session = Depends(get_db),
):
    artifact = (
        db.query(Artifact)
        .filter(Artifact.id == artifact_id)
        .first()
    )

    if artifact is None:
        raise HTTPException(
            status_code=404,
            detail="Artifact not found",
        )

    return artifact