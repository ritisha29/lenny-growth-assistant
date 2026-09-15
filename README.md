
### 4. `README.md`

```markdown
# Lenny Growth Assistant

AI-powered product and growth assistant grounded in Lenny's Podcast transcripts.

## What it does

Lenny Growth Assistant lets product and growth practitioners:

- ask questions about product and growth;
- continue conversations with follow-ups;
- see the transcript source behind answers;
- generate Ship 30 for 30 style essays;
- view generated Markdown artifacts beside the conversation;
- run the demo locally with Ollama.

## Architecture

```text
React
  ↓
FastAPI
  ↓
Agent Router
  ├── Ollama
  └── Anthropic Claude Agent SDK
  ↓
Retrieval
  ↓
ChromaDB
  ↓
Lenny Podcast transcripts

PostgreSQL
  ├── sessions
  ├── messages
  └── artifacts