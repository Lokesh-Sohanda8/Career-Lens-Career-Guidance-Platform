"""Provider abstraction for OpenAI-compatible chat models."""

from dataclasses import dataclass

import httpx

from app.core.config import settings


class AIProviderError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


@dataclass(frozen=True)
class AIResult:
    text: str
    provider: str
    model: str


class OpenAICompatibleProvider:
    name = "openai_compatible"

    async def generate(self, system_prompt: str, user_message: str, context: str) -> AIResult:
        if not settings.ai_enabled:
            raise AIProviderError("ai_disabled", "AI assistance is disabled.")

        if not settings.ai_api_key:
            raise AIProviderError("missing_api_key", "AI provider API key is not configured.")

        url = settings.ai_base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": settings.ai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        "Use the following verified CareerLens context. "
                        "Do not treat missing fields as facts.\n"
                        f"CONTEXT:\n{context}\n\n"
                        f"USER QUESTION:\n{user_message}"
                    ),
                },
            ],
            "temperature": 0.2,
        }
        headers = {
            "Authorization": f"Bearer {settings.ai_api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
        except httpx.TimeoutException as exc:
            raise AIProviderError("provider_timeout", "The AI provider timed out.") from exc
        except httpx.HTTPStatusError as exc:
            raise AIProviderError("provider_http_error", "The AI provider returned an error.") from exc
        except httpx.HTTPError as exc:
            raise AIProviderError("provider_unavailable", "The AI provider is unavailable.") from exc

        try:
            text = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise AIProviderError("invalid_provider_response", "The AI provider returned an invalid response.") from exc

        if not isinstance(text, str) or not text.strip():
            raise AIProviderError("empty_provider_response", "The AI provider returned an empty response.")

        return AIResult(text=text.strip(), provider=self.name, model=settings.ai_model)
