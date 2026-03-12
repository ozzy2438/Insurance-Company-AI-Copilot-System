from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class TeamContext(Base):
    __tablename__ = "team_contexts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    label: Mapped[str] = mapped_column(String, nullable=False)
    short_label: Mapped[str] = mapped_column(String, nullable=False)
    strapline: Mapped[str] = mapped_column(Text, nullable=False)
    operating_goal: Mapped[str] = mapped_column(Text, nullable=False)
    lead: Mapped[str] = mapped_column(String, nullable=False)
    live_experiments: Mapped[int] = mapped_column(Integer, nullable=False)
    adoption_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    governance_score: Mapped[int] = mapped_column(Integer, nullable=False)

    permission_scopes: Mapped[list["PermissionScope"]] = relationship(back_populates="team")


class Persona(Base):
    __tablename__ = "personas"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    default_team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    can_view_audit: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    default_team: Mapped[TeamContext] = relationship()
    permission_scopes: Mapped[list["PermissionScope"]] = relationship(back_populates="persona")


class PermissionScope(Base):
    __tablename__ = "permission_scopes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    persona_id: Mapped[str] = mapped_column(ForeignKey("personas.id"), nullable=False)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    can_review_governance: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    can_run_copilot: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    persona: Mapped[Persona] = relationship(back_populates="permission_scopes")
    team: Mapped[TeamContext] = relationship(back_populates="permission_scopes")


class Member(Base):
    __tablename__ = "members"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    segment: Mapped[str] = mapped_column(String, nullable=False)
    membership_tier: Mapped[str] = mapped_column(String, nullable=False)
    postcode: Mapped[str] = mapped_column(String, nullable=False)
    vulnerability_flags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    product_policies: Mapped[list["ProductPolicy"]] = relationship(back_populates="member")
    cases: Mapped[list["CaseRecord"]] = relationship(back_populates="member")


class ProductPolicy(Base):
    __tablename__ = "product_policies"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), nullable=False)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    product_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    renewal_date: Mapped[str] = mapped_column(String, nullable=False)
    coverage_summary: Mapped[str] = mapped_column(Text, nullable=False)

    member: Mapped[Member] = relationship(back_populates="product_policies")
    team: Mapped[TeamContext] = relationship()


class CaseRecord(Base):
    __tablename__ = "case_records"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), nullable=False)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    urgency: Mapped[str] = mapped_column(String, nullable=False)
    opened_at: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    assigned_team: Mapped[str] = mapped_column(String, nullable=False)
    owner: Mapped[str] = mapped_column(String, nullable=False)

    member: Mapped[Member] = relationship(back_populates="cases")
    team: Mapped[TeamContext] = relationship()
    interactions: Mapped[list["InteractionEvent"]] = relationship(back_populates="case", cascade="all, delete-orphan")
    scenarios: Mapped[list["ScenarioTemplate"]] = relationship(back_populates="case")


class InteractionEvent(Base):
    __tablename__ = "interaction_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("case_records.id"), nullable=False)
    channel: Mapped[str] = mapped_column(String, nullable=False)
    occurred_at: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    case: Mapped[CaseRecord] = relationship(back_populates="interactions")


class KnowledgeAsset(Base):
    __tablename__ = "knowledge_assets"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    usage_count: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)


class ScenarioTemplate(Base):
    __tablename__ = "scenario_templates"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    case_id: Mapped[str] = mapped_column(ForeignKey("case_records.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    member_moment: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    human_review_points: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    references: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    draft_output: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    canned_conversation: Mapped[list[dict[str, str]]] = mapped_column(JSON, default=list, nullable=False)
    linked_asset_ids: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    team: Mapped[TeamContext] = relationship()
    case: Mapped[CaseRecord] = relationship(back_populates="scenarios")


class ExperimentRecord(Base):
    __tablename__ = "experiment_records"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    owner: Mapped[str] = mapped_column(String, nullable=False)
    stage: Mapped[str] = mapped_column(String, nullable=False)
    risk: Mapped[str] = mapped_column(String, nullable=False)
    target_metric: Mapped[str] = mapped_column(String, nullable=False)
    baseline: Mapped[str] = mapped_column(String, nullable=False)
    pilot_result: Mapped[str] = mapped_column(String, nullable=False)
    decision: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    dependencies: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    linked_governance_ids: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    linked_knowledge_ids: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    timeline: Mapped[list[dict[str, str]]] = mapped_column(JSON, default=list, nullable=False)


class GovernanceReview(Base):
    __tablename__ = "governance_reviews"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    owner: Mapped[str] = mapped_column(String, nullable=False)
    risk: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    due_date: Mapped[str] = mapped_column(String, nullable=False)
    controls: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    exceptions: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    linked_experiment_ids: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)


class TrainingTrack(Base):
    __tablename__ = "training_tracks"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    audience: Mapped[str] = mapped_column(String, nullable=False)
    owner: Mapped[str] = mapped_column(String, nullable=False)
    completion: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    next_session: Mapped[str] = mapped_column(String, nullable=False)
    modules: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)


class AlertItem(Base):
    __tablename__ = "alert_items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    route: Mapped[str] = mapped_column(String, nullable=False)


class KpiSnapshot(Base):
    __tablename__ = "kpi_snapshots"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)
    change: Mapped[str] = mapped_column(String, nullable=False)
    direction: Mapped[str] = mapped_column(String, nullable=False)
    target: Mapped[str] = mapped_column(String, nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=False)


class ImpactStory(Base):
    __tablename__ = "impact_stories"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    baseline: Mapped[str] = mapped_column(String, nullable=False)
    current: Mapped[str] = mapped_column(String, nullable=False)
    evidence: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)


class CopilotRun(Base):
    __tablename__ = "copilot_runs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    persona_id: Mapped[str] = mapped_column(ForeignKey("personas.id"), nullable=False)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("scenario_templates.id"), nullable=False)
    case_id: Mapped[str] = mapped_column(ForeignKey("case_records.id"), nullable=False)
    mode: Mapped[str] = mapped_column(String, nullable=False)
    user_input: Mapped[str] = mapped_column(Text, nullable=False)
    provider_used: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_action: Mapped[str] = mapped_column(Text, nullable=False)
    draft: Mapped[str] = mapped_column(Text, nullable=False)
    citations: Mapped[list[dict[str, str]]] = mapped_column(JSON, default=list, nullable=False)
    risk_flags: Mapped[list[dict[str, str]]] = mapped_column(JSON, default=list, nullable=False)
    human_review_points: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    persona_id: Mapped[str] = mapped_column(ForeignKey("personas.id"), nullable=False)
    team_id: Mapped[str] = mapped_column(ForeignKey("team_contexts.id"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
