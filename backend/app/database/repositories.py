from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from app.database.models import Session


def create_session(
    db: DBSession,
    title: str | None = None,
) -> Session:
    session = Session(title=title)

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def list_sessions(
    db: DBSession,
) -> list[Session]:
    statement = (
        select(Session)
        .order_by(Session.updated_at.desc())
    )

    return list(db.scalars(statement).all())


def get_session(
    db: DBSession,
    session_id: str,
) -> Session | None:
    statement = select(Session).where(
        Session.id == session_id
    )

    return db.scalar(statement)

def create_message(db, session_id, role, content):
    from app.database.models import Message

    message = Message(
        session_id=session_id,
        role=role,
        content=content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def list_messages(db, session_id):
    from app.database.models import Message

    statement = (
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.created_at.asc())
    )

    return list(db.scalars(statement).all())

def create_artifact(
    db,
    session_id,
    artifact_type,
    content,
    message_id=None,
):
    from app.database.models import Artifact

    artifact = Artifact(
        session_id=session_id,
        message_id=message_id,
        artifact_type=artifact_type,
        content=content,
    )

    db.add(artifact)
    db.commit()
    db.refresh(artifact)

    return artifact