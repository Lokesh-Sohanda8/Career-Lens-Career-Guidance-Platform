"""Reports API schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ReportSectionCreate(BaseModel):
    section_key: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=300)
    content: str = Field(min_length=1)
    section_order: int = Field(ge=1)


class ReportCreate(BaseModel):
    report_type: str = Field(min_length=2, max_length=60)
    title: str = Field(min_length=1, max_length=300)
    source_snapshot: str = Field(min_length=2)
    sections: list[ReportSectionCreate] = Field(min_length=1)


class ReportSectionRead(BaseModel):
    id: uuid.UUID
    section_key: str
    title: str
    content: str
    section_order: int


class ReportRead(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    report_type: str
    title: str
    status: str
    version: int
    generated_at: datetime
    sections: list[ReportSectionRead]


class ReportSummaryRead(BaseModel):
    id: uuid.UUID
    report_type: str
    title: str
    status: str
    version: int
    generated_at: datetime
