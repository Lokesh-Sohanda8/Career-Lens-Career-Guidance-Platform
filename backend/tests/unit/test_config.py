from app.core.config import Settings


def test_cors_origins_are_parsed() -> None:
    settings = Settings(allowed_origins="http://localhost:3000, http://localhost:5173")
    assert settings.cors_origins == ["http://localhost:3000", "http://localhost:5173"]
