import google.generativeai as genai
from typing import AsyncGenerator
import asyncio
from ..config import get_settings

settings = get_settings()


class GeminiClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def generate_response(
        self,
        query: str,
        context: str,
        conversation_history: list = None
    ) -> str:
        system_prompt = """You are a document analyst. Answer questions based ONLY on the provided documents.
If the information is not in the documents, say "I don't have this information in the provided documents."
Be concise and accurate. Do not make up information."""

        prompt = f"{system_prompt}\n\nContext from documents:\n{context}\n\nUser Question: {query}"

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return f"Error generating response: {str(e)}"

    async def stream_response(
        self,
        query: str,
        context: str,
        conversation_history: list = None
    ) -> AsyncGenerator:
        system_prompt = """You are a document analyst. Answer questions based ONLY on the provided documents.
If the information is not in the documents, say "I don't have this information in the provided documents."
Be concise and accurate. Do not make up information."""

        prompt = f"{system_prompt}\n\nContext from documents:\n{context}\n\nUser Question: {query}"

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                stream=True
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error: {str(e)}"


gemini_client = None


def get_gemini_client():
    global gemini_client
    if gemini_client is None:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        gemini_client = GeminiClient(settings.gemini_api_key)
    return gemini_client
