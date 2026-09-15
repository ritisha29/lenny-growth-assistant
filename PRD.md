# Lenny Growth Assistant — Product Requirements Document

## 1. Product Overview

Lenny Growth Assistant is an AI-powered conversational assistant for product and growth practitioners.

It uses Lenny's Podcast transcript corpus as a knowledge base so users can ask product and growth questions and receive grounded answers based on Lenny's content.

The product also provides a dedicated Ship 30 for 30 writing capability that turns relevant transcript evidence into a polished Markdown essay displayed in an Artifact Viewer.

## 2. User Problem

Product and growth practitioners often have access to a large amount of high-quality content but struggle to quickly find the specific insight they need.

The problem is not simply finding transcripts. Users need to:

- ask questions in natural language;
- receive answers grounded in the source material;
- ask follow-up questions without losing context;
- understand which episode supports an answer;
- turn useful insights into reusable written content.

The assistant reduces the time between having a product/growth question and finding a grounded, actionable answer.

## 3. Target User

Primary users are:

- Product managers
- Growth practitioners
- Startup founders
- Product leaders
- Researchers interested in Lenny's Podcast content

## 4. Goals

### Primary goal

Help a user get a trustworthy answer to a product or growth question using Lenny's Podcast transcripts.

### Secondary goals

- Preserve conversation context across follow-up questions.
- Show source information for generated answers.
- Generate a Ship 30 for 30 style essay from transcript evidence.
- Render generated content as a native artifact.
- Support local LLM inference through Ollama for the demo.
- Keep the architecture flexible enough to support cloud models.

## 5. Success Metric

### Primary measurable success metric

**Grounded Answer Success Rate**

Percentage of evaluation questions for which the assistant produces an answer that is supported by the retrieved transcript evidence and identifies the relevant source.

Target for the take-home:

> ≥80% grounded-answer success across a manually curated evaluation set.

### Secondary metrics

- Time to first response
- Percentage of questions with identifiable sources
- Successful Ship 30 artifact generation rate
- API error rate
- Session persistence success rate

## 6. Product Experience

The main interface contains three areas:

1. **Conversation sidebar**
   - Start a new conversation
   - View the active conversation
   - Launch Ship 30 generation

2. **Chat**
   - Ask product and growth questions
   - Continue conversations with follow-ups
   - See grounded sources attached to responses

3. **Artifact Viewer**
   - Display generated Markdown content
   - Keep generated content visible beside the conversation

## 7. Core User Stories

### Conversational Q&A

As a product practitioner, I want to ask a product or growth question so that I can quickly learn from Lenny's content.

### Follow-up questions

As a user, I want to ask follow-up questions so that I can explore an idea without repeating the original context.

### Source tracing

As a user, I want to see which episode supports an answer so that I can validate and explore the source.

### Ship 30 generation

As a user, I want to turn transcript evidence into a polished essay so that I can reuse the insight as written content.

### Local model demo

As an evaluator, I want the application to run with Ollama so that the complete product can be demonstrated without requiring a cloud API key.

## 8. Scope

### In scope

- React web interface
- FastAPI backend
- PostgreSQL persistence
- Podcast transcript ingestion
- Vector retrieval with ChromaDB
- Grounded conversational Q&A
- Conversation history
- Source metadata
- Ollama integration
- Anthropic Claude Agent SDK integration
- Ship 30 for 30 skill
- Markdown artifact generation
- Artifact Viewer
- Health endpoint
- Environment-based configuration

### Out of scope

- Multi-user authentication
- Production billing
- Advanced permissions
- Real-time collaboration
- Full document editing
- Automatic transcript crawling on every request
- Mobile-native applications

## 9. Key Assumptions

- Lenny's transcript repository is a sufficient initial knowledge source.
- Users prefer conversational retrieval over manually searching transcripts.
- Local Ollama inference is acceptable for demonstration.
- PostgreSQL is sufficient for session and artifact persistence.
- ChromaDB provides adequate retrieval quality for the initial corpus.

## 10. Risks and Tradeoffs

### Hallucination

A small local model can generate claims that are not fully supported by retrieved evidence.

Mitigation:

- Explicit grounding instructions
- Transcript-only context
- Source metadata
- Insufficient-evidence behavior

### Retrieval quality

Semantic retrieval can return related but incorrect passages, particularly for ambiguous follow-up references.

Mitigation:

- Conversation history is included in retrieval queries.
- Candidate retrieval is combined with lexical matching.
- Future improvement: dedicated conversational reference resolution.

### Latency

Local model inference can be slower on CPU-only hardware.

Tradeoff:

- Ollama provides a no-cost local demo.
- Cloud providers can provide better latency and quality.

### Cost

Cloud inference introduces API costs.

Tradeoff:

- Provider selection is configuration-driven.
- Ollama is used for the demo.

### Data leakage

User conversations should not accidentally become part of the transcript knowledge base.

Mitigation:

- Transcript ingestion is a separate process.
- User messages are persisted in PostgreSQL but are not indexed into the transcript collection.

### Unsafe artifact rendering

Generated HTML could contain unsafe content.

Mitigation:

- Initial artifact format is Markdown.
- If HTML artifacts are added, they should be sanitized and rendered in an isolated sandbox.

## 11. Product Decisions

### Why Markdown first?

Markdown provides rich formatting while avoiding the security risks of directly rendering arbitrary generated HTML.

### Why Ollama?

Ollama makes the demo reproducible without requiring an external API key and satisfies the local-model requirement.

### Why PostgreSQL?

It provides durable relational persistence for sessions, messages, artifacts, and source relationships.

### Why ChromaDB?

It provides a simple persistent vector store suitable for a take-home application and local development.

## 12. Future Improvements

- Better conversational reference resolution
- Hybrid retrieval with stronger reranking
- Streaming model responses
- More cloud providers
- Evaluation dashboard
- Authentication
- Background ingestion jobs
- Artifact editing
- HTML artifact support with sandboxing