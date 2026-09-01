"""AI assistance orchestration.

The service coordinates canonical context, guardrails, provider execution,
and audit logging. It does not own business truth.
"""

import hashlib
import time

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.domains.ai.context import AIContextBuilder
from app.domains.ai.guardrails import AIGuardrails
from app.domains.ai.provider import AIProviderError, OpenAICompatibleProvider
from app.domains.ai.repository import AIRepository
from app.domains.student.service import StudentService


class AIService:
    PROMPT_VERSION = "v1"

    def __init__(self, session: AsyncSession):
        self.session = session
        self.students = StudentService(session)
        self.context_builder = AIContextBuilder(session)
        self.repo = AIRepository(session)
        self.provider = OpenAICompatibleProvider()

    async def ask(self, user_id, message, task_type):
        student = await self.students.get_for_user(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found.")

        guardrail = AIGuardrails.validate_user_message(message)
        if not guardrail.allowed:
            raise HTTPException(status_code=400, detail=guardrail.message)

        context_payload = await self.context_builder.build_for_student(student.id)
        context = self.context_builder.to_prompt_context(context_payload)
        input_hash = hashlib.sha256(
            (context + "\n" + message).encode("utf-8")
        ).hexdigest()

        started = time.perf_counter()
        try:
            result = await self.provider.generate(
                AIGuardrails.system_policy(),
                message,
                context,
            )
            status = "completed"
            error_code = None
        except AIProviderError as exc:
            result = None
            status = "failed"
            error_code = exc.code

        latency_ms = int((time.perf_counter() - started) * 1000)
        interaction = await self.repo.create(
            student_id=student.id,
            task_type=task_type,
            provider=settings.ai_provider,
            model=settings.ai_model,
            prompt_version=self.PROMPT_VERSION,
            context_version=self.context_builder.VERSION,
            input_hash=input_hash,
            response_text=result.text if result else None,
            status=status,
            latency_ms=latency_ms,
            error_code=error_code,
        )

        await self.session.commit()

        if not result:
            raise HTTPException(
                status_code=503,
                detail="AI assistance is temporarily unavailable.",
            )

        return interaction, result
