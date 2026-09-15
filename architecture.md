# Architecture

## System Overview

```text
┌──────────────────────────────┐
│        React Frontend        │
│                              │
│ Chat | Sessions | Sources    │
│ Artifact Viewer | Model UI   │
└──────────────┬───────────────┘
               │ REST
               ▼
┌──────────────────────────────┐
│          FastAPI             │
│                              │
│ Sessions | Chat | Ship30     │
│ Artifacts | Health           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Agent Layer          │
│                              │
│ Agent Router                 │
│ ├── Conversational QA        │
│ ├── Ship 30 Skill            │
│ └── Artifact Generation      │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│ Retrieval   │  │ LLM Layer   │
│             │  │             │
│ ChromaDB    │  │ Ollama      │
│ + embeddings│  │ Claude SDK  │
└──────┬──────┘  └─────────────┘
       │
       ▼
┌──────────────────────────────┐
│     Lenny Transcript KB      │
│                              │
│ Podcast Markdown transcripts │
└──────────────────────────────┘

              PostgreSQL
                 ▲
                 │
       sessions / messages /
       artifacts / sources