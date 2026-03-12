from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


TeamId = Literal["roadside", "claims", "contact-centre"]


def to_camel(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(item.capitalize() for item in tail)


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class TeamContextOut(ApiModel):
    id: TeamId
    label: str
    short_label: str
    strapline: str
    operating_goal: str
    lead: str
    live_experiments: int
    adoption_rate: int
    governance_score: int


class PermissionScopeOut(ApiModel):
    team_id: TeamId
    can_review_governance: bool
    can_run_copilot: bool


class PersonaOut(ApiModel):
    id: str
    name: str
    title: str
    description: str
    default_team_id: TeamId
    can_view_audit: bool
    permission_scopes: list[PermissionScopeOut]


class SessionResponse(ApiModel):
    active_persona: PersonaOut
    personas: list[PersonaOut]
    accessible_teams: list[TeamContextOut]


class KpiMetricOut(ApiModel):
    id: str
    team: TeamId
    label: str
    value: str
    change: str
    direction: str
    target: str
    note: str


class AlertItemOut(ApiModel):
    id: str
    team: TeamId
    severity: str
    title: str
    body: str
    route: str


class ScenarioReferenceOut(ApiModel):
    title: str
    type: str
    detail: str


class ScenarioTemplateOut(ApiModel):
    id: str
    team: TeamId
    case_id: str
    title: str
    member_moment: str
    summary: str
    objective: str
    recommended_prompt: str
    human_review_points: list[str]
    references: list[ScenarioReferenceOut]
    draft_output: list[str]
    canned_conversation: list[dict[str, str]]
    linked_asset_ids: list[str]


class ExperimentRecordOut(ApiModel):
    id: str
    team: TeamId
    name: str
    owner: str
    stage: str
    risk: str
    target_metric: str
    baseline: str
    pilot_result: str
    decision: str
    summary: str
    dependencies: list[str]
    linked_governance_ids: list[str]
    linked_knowledge_ids: list[str]
    timeline: list[dict[str, str]]


class GovernanceReviewOut(ApiModel):
    id: str
    team: TeamId
    title: str
    owner: str
    risk: str
    status: str
    due_date: str
    controls: list[str]
    exceptions: list[str]
    linked_experiment_ids: list[str]


class KnowledgeAssetOut(ApiModel):
    id: str
    team: TeamId
    type: str
    title: str
    description: str
    owner: str
    status: str
    tags: list[str]
    usage_count: int
    rating: float
    excerpt: str


class TrainingTrackOut(ApiModel):
    id: str
    team: TeamId
    title: str
    audience: str
    owner: str
    completion: int
    status: str
    next_session: str
    modules: list[str]


class ImpactStoryOut(ApiModel):
    id: str
    team: TeamId
    title: str
    baseline: str
    current: str
    evidence: list[str]


class MemberProfileOut(ApiModel):
    id: str
    full_name: str
    segment: str
    membership_tier: str
    postcode: str
    vulnerability_flags: list[str]


class ProductPolicyOut(ApiModel):
    id: str
    team: TeamId
    product_name: str
    status: str
    renewal_date: str
    coverage_summary: str


class InteractionEventOut(ApiModel):
    id: int
    channel: str
    occurred_at: str
    summary: str


class CaseRecordOut(ApiModel):
    id: str
    member_id: str
    team: TeamId
    title: str
    status: str
    urgency: str
    opened_at: str
    summary: str
    assigned_team: str
    owner: str


class CaseContextResponse(ApiModel):
    case_record: CaseRecordOut
    member: MemberProfileOut
    product_policies: list[ProductPolicyOut]
    interactions: list[InteractionEventOut]


class OverviewResponse(ApiModel):
    team: TeamContextOut
    kpis: list[KpiMetricOut]
    alerts: list[AlertItemOut]
    scenarios: list[ScenarioTemplateOut]
    scale_candidates: list[ExperimentRecordOut]
    training_tracks: list[TrainingTrackOut]
    knowledge_assets: list[KnowledgeAssetOut]


class AcademyResponse(ApiModel):
    team: TeamContextOut
    training_tracks: list[TrainingTrackOut]


class ImpactResponse(ApiModel):
    team: TeamContextOut
    kpis: list[KpiMetricOut]
    stories: list[ImpactStoryOut]


class CitationOut(ApiModel):
    title: str
    type: str
    detail: str


class RiskFlagOut(ApiModel):
    level: str
    text: str


class CopilotRunRequest(ApiModel):
    team_id: TeamId
    scenario_id: str
    case_id: str
    mode: Literal["demo", "live"]
    user_input: str = Field(min_length=3)


class CopilotRunResult(ApiModel):
    run_id: str
    audit_event_id: str
    provider_used: str
    summary: str
    recommended_action: str
    draft: str
    citations: list[CitationOut]
    risk_flags: list[RiskFlagOut]
    human_review_points: list[str]


class ActionRequest(ApiModel):
    action: str = Field(min_length=2)
    detail: str = Field(min_length=3)


class ActionResponse(ApiModel):
    status: str
    audit_event_id: str


class AuditEventOut(ApiModel):
    id: str
    persona_id: str
    team_id: TeamId
    entity_type: str
    entity_id: str
    action: str
    detail: str
    created_at: datetime
