"""Counselling Intelligence endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domains.counselling.schemas import (
    ActionItemCreate, ActionItemRead, ActionItemUpdate,
    DecisionCreate, DecisionRead, GoalCreate, GoalRead, GoalUpdate,
    NoteCreate, NoteRead, SessionCreate, SessionRead, SessionUpdate,
)
from app.domains.counselling.service import CounsellingService

router = APIRouter(prefix="/counselling", tags=["Counselling"])


@router.get("/sessions", response_model=list[SessionRead])
async def list_sessions(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CounsellingService(db).sessions(user.id)


@router.post("/sessions", response_model=SessionRead, status_code=201)
async def create_session(payload: SessionCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CounsellingService(db).create_session(user.id, payload)


@router.patch("/sessions/{session_id}", response_model=SessionRead)
async def update_session(session_id: UUID, payload: SessionUpdate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CounsellingService(db).update_session(user.id, session_id, payload)


@router.post("/sessions/{session_id}/notes", response_model=NoteRead, status_code=201)
async def add_note(session_id: UUID, payload: NoteCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CounsellingService(db).add_note(user.id, session_id, payload)


@router.post("/sessions/{session_id}/decisions", response_model=DecisionRead, status_code=201)
async def add_decision(session_id: UUID, payload: DecisionCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CounsellingService(db).add_decision(user.id, session_id, payload)


@router.post("/sessions/{session_id}/actions", response_model=ActionItemRead, status_code=201)
async def add_action(session_id: UUID, payload: ActionItemCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CounsellingService(db).add_action_item(user.id, session_id, payload)


@router.patch("/actions/{action_id}", response_model=ActionItemRead)
async def update_action(action_id: UUID, payload: ActionItemUpdate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CounsellingService(db).update_action_item(user.id, action_id, payload)


@router.get("/goals", response_model=list[GoalRead])
async def list_goals(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CounsellingService(db).goals(user.id)


@router.post("/goals", response_model=GoalRead, status_code=201)
async def create_goal(payload: GoalCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CounsellingService(db).create_goal(user.id, payload)


@router.patch("/goals/{goal_id}", response_model=GoalRead)
async def update_goal(goal_id: UUID, payload: GoalUpdate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CounsellingService(db).update_goal(user.id, goal_id, payload)
