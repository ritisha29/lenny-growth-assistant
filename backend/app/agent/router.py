from app.agent.agent import ClaudeAgent
from app.agent.skills.ship30.skill import Ship30Skill
from app.config import settings
from app.llm.ollama import OllamaClient


class AgentRouter:
    def __init__(self):
        self.ollama = OllamaClient()
        self.claude = ClaudeAgent()
        self.ship30 = Ship30Skill()

    async def generate(self, prompt: str) -> str:
        provider = settings.llm_provider.lower()

        if provider == "ollama":
            return await self.ollama.generate(prompt)

        if provider == "anthropic":
            return await self.claude.generate(prompt)

        raise ValueError(
            f"Unsupported LLM_PROVIDER: {settings.llm_provider}"
        )

    async def generate_ship30(
        self,
        topic: str,
        source_url: str | None = None,
    ) -> str:
        prompt, _ = self.ship30.build_prompt(
            topic=topic,
            source_url=source_url,
        )

        return await self.generate(prompt)