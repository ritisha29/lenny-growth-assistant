from app.retrieval.search import TranscriptRetriever


class Ship30Skill:
    """
    Dedicated writing skill for generating a grounded
    Ship 30 for 30 style essay from Lenny transcript evidence.
    """

    def __init__(self):
        self.retriever = TranscriptRetriever()

    def build_prompt(
        self,
        topic: str,
        source_url: str | None = None,
    ) -> tuple[str, list[dict]]:

        query = topic

        if source_url:
            query = f"{topic} {source_url}"

        results = self.retriever.search(
            query,
            top_k=8,
        )
        # If the user supplied a source URL, keep only transcript chunks
        # belonging to that exact source.
        if source_url:
            filtered_results = [
                result
                for result in results
                if result["metadata"].get("source_url") == source_url
            ]

            if filtered_results:
                results = filtered_results

        if not results:
            raise ValueError(
                "I couldn't find enough evidence in Lenny's transcripts "
                "to create this Ship 30 for 30 essay."
            )

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

        prompt = f"""You are Lenny's Growth Assistant creating a
Ship 30 for 30 style essay.

TOPIC
=====

{topic}

WRITING PRINCIPLES
==================

Write a complete Ship 30 for 30 style essay, not a summary.

The essay should be approximately 1,250 words.

Structure the essay like this:

1. Start with a compelling hook that creates curiosity about the problem.
2. Introduce the central problem or tension.
3. Develop the main insight from the transcript as a narrative.
4. Explain the important ideas from the source in a logical sequence.
5. Use clear Markdown headings to make the essay easy to scan.
6. Use short paragraphs rather than long blocks of text.
7. Use bullets only when they genuinely improve readability.
8. Use selective **bold** emphasis for important ideas.
9. End with a practical takeaway for the reader.

Do NOT format the essay as a numbered list of transcript points.

Do NOT write a summary of the transcript.

Do NOT begin with phrases such as:
- "This is a transcript excerpt..."
- "Here's a summary..."
- "The key points are..."
- "Overall, the conversation highlights..."

Instead, write as a polished standalone article for a product or growth practitioner.

GROUNDING RULES
===============

- Use ONLY the transcript evidence provided below.
- Do not use outside knowledge.
- Do not invent facts, quotes, examples, stories, frameworks,
  or recommendations.
- Do not attribute an idea to a person unless the transcript
  supports that attribution.
- Paraphrase transcript material rather than inventing quotations.
- Preserve the meaning of the source while turning it into a coherent
  narrative.
- If the evidence is insufficient to support an important part of
  the requested essay, say so rather than filling the gap.
- The writing style may be polished and engaging, but every factual
  claim must remain faithful to the transcript evidence.
- Do not mention these instructions in the essay.

TRANSCRIPT EVIDENCE
===================

{context}
"""

        return prompt, results