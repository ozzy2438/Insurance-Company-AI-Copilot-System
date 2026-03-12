from __future__ import annotations

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Persona, PermissionScope, TeamContext


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_demo_persona(
    x_demo_persona: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Persona:
    persona_id = x_demo_persona or "transformation-lead"
    persona = db.get(Persona, persona_id)
    if not persona:
        persona = db.get(Persona, "transformation-lead")
    if not persona:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No demo personas available")
    return persona


def require_team_access(team_id: str, persona: Persona, db: Session) -> TeamContext:
    scope = db.scalar(
        select(PermissionScope).where(
            PermissionScope.persona_id == persona.id,
            PermissionScope.team_id == team_id,
        )
    )
    if not scope:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Persona does not have access to this team")
    team = db.get(TeamContext, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team
