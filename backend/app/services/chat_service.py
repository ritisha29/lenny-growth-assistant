from app.database.repositories import (
    create_message,
    get_session,
    list_messages,
)
from app.agent.router import AgentRouter
from app.retrieval.search import TranscriptRetriever


class ChatService:
    def __init__(self):
        self.retriever = TranscriptRetriever()
        self.llm = AgentRouter()

    async def answer(self, session_id: str, question: str, db) -> dict:
        session = get_session(db, session_id)

        if session is None:
            raise ValueError("Session not found")

        # Save the user's message
        create_message(
            db=db,
            session_id=session_id,
            role="user",
            content=question,
        )

        # Load previous conversation messages for this session
        conversation_messages = list_messages(
            db=db,
            session_id=session_id,
        )

        # Use recent conversation context to improve retrieval for follow-up questions
        retrieval_query = question

        if conversation_messages:
            previous_messages = conversation_messages[-4:]

            previous_context = "\n".join(
                f"{message.role}: {message.content}"
                for message in previous_messages
                if message.content
            )

            retrieval_query = f"""
        Previous conversation:
        {previous_context}

        Current question:
        {question}
        """

        # Retrieve relevant transcript evidence
        results = self.retriever.search(retrieval_query, top_k=5)

        if not results:
            answer = (
                "I couldn't find relevant evidence in Lenny's transcripts "
                "to answer that question."
            )

            create_message(
                db=db,
                session_id=session_id,
                role="assistant",
                content=answer,
            )

            return {
                "answer": answer,
                "sources": [],
            }

        context_parts = []

        for index, result in enumerate(results, start=1):
            metadata = result["metadata"]

            context_parts.append(
                f"""SOURCE {index}
Episode: {metadata.get("episode_title", "Unknown")}
Guest: {metadata.get("guest", "Unknown")}
Date: {metadata.get("date", "Unknown")}
Source URL: {metadata.get("source_url", "")}

Transcript excerpt:
{result["text"]}
"""
            )

        context = "\n\n".join(context_parts)
        history_parts = []

        for message in conversation_messages[:-1]:
            history_parts.append(
                f"{message.role.upper()}: {message.content}"
            )

        conversation_history = "\n".join(history_parts)

        if not conversation_history:
            conversation_history = "(No previous conversation.)"

        prompt = f"""You are Lenny's Growth Assistant.

Answer the user's question using the transcript excerpts and the conversation history provided below.

Use the conversation history to understand references such as "you mentioned",
"the first one", "that framework", or "what did you just say".
- When the user asks a follow-up about something already stated in the
  conversation, use the previous assistant answer as the primary reference.
- For questions such as "what was the first one?", "what did you just say?",
  or "what was the second point?", answer from the previous assistant answer
  when it contains the requested information.
- Do not reinterpret a conversational reference by selecting a different
  sentence from the transcript.

When the user is referring to something from a previous assistant answer,
preserve the meaning of that previous answer. Use the transcript evidence
to verify it, but do not replace it with an unrelated passage from the same
episode.

Important rules:
- Do not use outside knowledge.
- Do not invent facts, quotes, or recommendations.
- Every factual claim in the answer must be directly supported by
  the provided transcript excerpts or the conversation history.
- When answering a numbered framework or list, reproduce only items
  that are explicitly supported by the evidence.
- Do not infer missing framework items from the topic, title, or
  general knowledge.
- Do not add examples, tactics, explanations, or conclusions unless
  they are explicitly supported by the evidence.
- If you cannot confidently support an item from the evidence, omit it
  and state that the available excerpts do not provide enough evidence.
- If the user asks for a numbered list, framework, checklist, steps,
  or specific number of items, include only items explicitly supported
  by the transcript evidence.
- Never create a plausible-sounding replacement item when evidence
  for an item is missing.
- Do not add explanations, examples, tactics, or recommendations unless
  they are explicitly supported by the provided transcript excerpts.
- If the transcript gives only the name of a framework item, report the
  item without inventing an explanation for it.
- If the transcripts do not provide enough evidence, clearly say that you
  don't have enough evidence from the available Lenny transcripts.
- Prefer specific ideas from the sources over generic advice.
- Do not claim that something came from Lenny's content unless it is supported
  by the provided excerpts.
- Write a useful, concise answer.
- Do not include a separate sources section; sources are returned separately
  by the application.
- For questions asking for a specific number of items, return only the
  requested items and their transcript-supported descriptions. Do not add
  a concluding interpretation unless the transcript explicitly supports it.

CONVERSATION HISTORY
====================

{conversation_history}

TRANSCRIPT EVIDENCE
===================

{context}

USER QUESTION
=============

{question}
"""

        # Generate the grounded answer
        answer = await self.llm.generate(prompt)

        # Save the assistant's message
        create_message(
            db=db,
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        # Deduplicate sources
        sources = []
        seen_sources = set()

        for result in results:
            metadata = result["metadata"]

            source_key = (
                metadata.get("episode_title"),
                metadata.get("source_url"),
            )

            if source_key in seen_sources:
                continue

            seen_sources.add(source_key)

            sources.append(
                {
                    "episode_title": metadata.get(
                        "episode_title",
                        "Unknown",
                    ),
                    "guest": metadata.get("guest"),
                    "date": metadata.get("date"),
                    "source_url": metadata.get("source_url"),
                }
            )

        return {
            "answer": answer,
            "sources": sources,
        }