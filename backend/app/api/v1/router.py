"""Version 1 API router."""

from fastapi import APIRouter

from app.api.v1 import (
    assessments, auth, ai, careers, counselling, education, health, learning,
    recommendations, reports, skills, students, users,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(students.router)
api_router.include_router(assessments.router)
api_router.include_router(careers.router)
api_router.include_router(skills.router)
api_router.include_router(recommendations.router)
api_router.include_router(education.router)
api_router.include_router(learning.router)
api_router.include_router(counselling.router)
api_router.include_router(reports.router)
api_router.include_router(ai.router)
