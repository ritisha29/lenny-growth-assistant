from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.sessions import router as sessions_router
from app.api.chat import router as chat_router
from app.api.ship30 import router as ship30_router
from app.api.artifacts import router as artifacts_router


from app.database.session import get_db


app = FastAPI(
    title="Lenny Growth Assistant",
    description="AI-powered product and growth assistant grounded in Lenny's Podcast transcripts.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router)
app.include_router(chat_router)
app.include_router(ship30_router)
app.include_router(artifacts_router)


@app.get("/")
async def root():
    return {
        "message": "Lenny Growth Assistant API"
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected",
        }

    except Exception:
        return {
            "status": "error",
            "database": "unavailable",
        }
    