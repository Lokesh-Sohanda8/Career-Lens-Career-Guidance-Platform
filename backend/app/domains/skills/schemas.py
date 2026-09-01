"""Skill Intelligence API schemas."""
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
class SkillCategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID; code: str; name: str; description: str | None
class SkillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID; code: str; name: str; description: str | None; is_active: bool; category: SkillCategoryRead | None
class SkillEvidenceUpsert(BaseModel):
    skill_id: uuid.UUID
    level: int = Field(ge=0, le=5)
    confidence: int = Field(default=3, ge=1, le=5)
    source_type: str = Field(min_length=2, max_length=50)
    evidence_note: str | None = Field(default=None, max_length=2000)
class StudentSkillEvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID; skill_id: uuid.UUID; level: int; confidence: int; source_type: str; evidence_note: str | None; created_at: datetime; updated_at: datetime
class SkillGapRead(BaseModel):
    skill_id: uuid.UUID; skill_name: str; required_level: int; current_level: int; gap: int; importance: int; priority_score: float; evidence_source: str | None
