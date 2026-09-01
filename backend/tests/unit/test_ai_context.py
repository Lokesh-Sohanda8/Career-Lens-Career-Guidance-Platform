from app.domains.ai.context import AIContextBuilder


def test_context_serialization_is_deterministic():
    payload = {"student": {"first_name": "A"}, "goals": []}
    first = AIContextBuilder.to_prompt_context(payload)
    second = AIContextBuilder.to_prompt_context(payload)
    assert first == second
    assert '"first_name":"A"' in first
