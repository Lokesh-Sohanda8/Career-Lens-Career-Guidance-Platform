from app.core.config import Settings
from app.domains.identity.schemas import UserCreate
from app.domains.identity.service import IdentityService


def test_identity_security_settings_exist():
    settings = Settings(secret_key="a" * 32)
    assert settings.algorithm == "HS256"
    assert settings.access_token_expire_minutes == 60


def test_identity_password_contract_matches_bcrypt_limit():
    assert UserCreate(email="student@example.com", password="a" * 72).password == "a" * 72


def test_identity_default_role_is_student():
    assert IdentityService.DEFAULT_STUDENT_ROLE == "student"
