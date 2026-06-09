from anthropic import Anthropic, AsyncAnthropic
from typing import List, AsyncGenerator
from ..config import get_settings

settings = get_settings()


class ClaudeClient:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.claude_api_key)
        self.model = settings.claude_model

    async def generate_response(
        self,
        query: str,
        context: str,
        conversation_history: List[dict] = None
    ) -> str:
        system_prompt = """You are a document analyst. Answer questions based ONLY on the provided documents.
If the information is not in the documents, say "I don't have this information in the provided documents."
Be concise and accurate."""

        messages = conversation_history or []
        messages.append({
            "role": "user",
            "content": f"Context from documents:\n{context}\n\nQuestion: {query}"
        })

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )

        return response.content[0].text

    async def stream_response(
        self,
        query: str,
        context: str,
        conversation_history: List[dict] = None
    ) -> AsyncGenerator:
        system_prompt = """You are a document analyst. Answer questions based ONLY on the provided documents.
If the information is not in the documents, say "I don't have this information in the provided documents."
Be concise and accurate."""

        messages = conversation_history or []
        messages.append({
            "role": "user",
            "content": f"Context from documents:\n{context}\n\nQuestion: {query}"
        })

        with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        ) as stream:
            for text in stream.text_stream:
                yield text


claude_client = None


def get_claude_client():
    global claude_client
    if claude_client is None:
        claude_client = ClaudeClient()
    return claude_client
