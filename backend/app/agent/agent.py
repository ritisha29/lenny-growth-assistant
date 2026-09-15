from claude_agent_sdk import ClaudeAgentOptions, query

from app.config import settings


class ClaudeAgent:
    async def generate(self, prompt: str) -> str:
        if not settings.anthropic_api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not configured."
            )

        options = ClaudeAgentOptions(
            model="claude-sonnet-4-5",
            permission_mode="bypassPermissions",
        )

        response_parts = []

        async for message in query(
            prompt=prompt,
            options=options,
        ):
            if hasattr(message, "result"):
                response_parts.append(message.result)

        if not response_parts:
            raise RuntimeError(
                "Claude Agent SDK returned no response."
            )

        return "\n".join(response_parts)