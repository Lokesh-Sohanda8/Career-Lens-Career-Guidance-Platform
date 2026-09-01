import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.integration
def test_readiness_endpoint_exists() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    assert response.json()["status"] in {"ready", "not_ready"}
