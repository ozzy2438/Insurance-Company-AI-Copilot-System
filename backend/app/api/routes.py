from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from ..models import (
    AlertItem,
    AuditEvent,
    CaseRecord,
    CopilotRun,
    ExperimentRecord,
    GovernanceReview,
    ImpactStory,
    InteractionEvent,
    KnowledgeAsset,
    KpiSnapshot,
    Member,
    PermissionScope,
    Persona,
    ProductPolicy,
    ScenarioTemplate,
    TeamContext,
    TrainingTrack,
)
from ..schemas import (
    AcademyResponse,
    ActionRequest,
    ActionResponse,
    AlertItemOut,
    AuditEventOut,
    CaseContextResponse,
    CaseRecordOut,
    CopilotRunRequest,
    CopilotRunResult,
    ExperimentRecordOut,
    GovernanceReviewOut,
    ImpactResponse,
    ImpactStoryOut,
    InteractionEventOut,
    KpiMetricOut,
    KnowledgeAssetOut,
    MemberProfileOut,
    OverviewResponse,
    PermissionScopeOut,
    PersonaOut,
    ProductPolicyOut,
    ScenarioTemplateOut,
    SessionResponse,
    TeamContextOut,
    TrainingTrackOut,
)
from ..services.orchestration import create_copilot_result
from .deps import get_db, get_demo_persona, require_team_access

router = APIRouter(prefix="/api")


def _team_out(team: TeamContext) -> TeamContextOut:
    return TeamContextOut.model_validate(team, from_attributes=True)


def _persona_out(persona: Persona, scopes: list[PermissionScope]) -> PersonaOut:
    return PersonaOut(
        id=persona.id,
        name=persona.name,
        title=persona.title,
        description=persona.description,
        default_team_id=persona.default_team_id,
        can_view_audit=persona.can_view_audit,
        permission_scopes=[
            PermissionScopeOut(
                team_id=scope.team_id,
                can_review_governance=scope.can_review_governance,
                can_run_copilot=scope.can_run_copilot,
            )
            for scope in scopes
        ],
    )


def _scenario_out(item: ScenarioTemplate) -> ScenarioTemplateOut:
    return ScenarioTemplateOut(
        id=item.id,
        team=item.team_id,
        case_id=item.case_id,
        title=item.title,
        member_moment=item.member_moment,
        summary=item.summary,
        objective=item.objective,
        recommended_prompt=item.recommended_prompt,
        human_review_points=item.human_review_points,
        references=item.references,
        draft_output=item.draft_output,
        canned_conversation=item.canned_conversation,
        linked_asset_ids=item.linked_asset_ids,
    )


def _experiment_out(item: ExperimentRecord) -> ExperimentRecordOut:
    return ExperimentRecordOut(
        id=item.id,
        team=item.team_id,
        name=item.name,
        owner=item.owner,
        stage=item.stage,
        risk=item.risk,
        target_metric=item.target_metric,
        baseline=item.baseline,
        pilot_result=item.pilot_result,
        decision=item.decision,
        summary=item.summary,
        dependencies=item.dependencies,
        linked_governance_ids=item.linked_governance_ids,
        linked_knowledge_ids=item.linked_knowledge_ids,
        timeline=item.timeline,
    )


def _governance_out(item: GovernanceReview) -> GovernanceReviewOut:
    return GovernanceReviewOut(
        id=item.id,
        team=item.team_id,
        title=item.title,
        owner=item.owner,
        risk=item.risk,
        status=item.status,
        due_date=item.due_date,
        controls=item.controls,
        exceptions=item.exceptions,
        linked_experiment_ids=item.linked_experiment_ids,
    )


def _asset_out(item: KnowledgeAsset) -> KnowledgeAssetOut:
    return KnowledgeAssetOut(
        id=item.id,
        team=item.team_id,
        type=item.type,
        title=item.title,
        description=item.description,
        owner=item.owner,
        status=item.status,
        tags=item.tags,
        usage_count=item.usage_count,
        rating=item.rating,
        excerpt=item.excerpt,
    )


def _track_out(item: TrainingTrack) -> TrainingTrackOut:
    return TrainingTrackOut(
        id=item.id,
        team=item.team_id,
        title=item.title,
        audience=item.audience,
        owner=item.owner,
        completion=item.completion,
        status=item.status,
        next_session=item.next_session,
        modules=item.modules,
    )


def _kpi_out(item: KpiSnapshot) -> KpiMetricOut:
    return KpiMetricOut(
        id=item.id,
        team=item.team_id,
        label=item.label,
        value=item.value,
        change=item.change,
        direction=item.direction,
        target=item.target,
        note=item.note,
    )


def _alert_out(item: AlertItem) -> AlertItemOut:
    return AlertItemOut(id=item.id, team=item.team_id, severity=item.severity, title=item.title, body=item.body, route=item.route)


@router.get("/session", response_model=SessionResponse)
def get_session(persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)) -> SessionResponse:
    personas = db.scalars(select(Persona).order_by(Persona.name)).all()
    all_scopes = db.scalars(select(PermissionScope)).all()
    scopes_by_persona: dict[str, list[PermissionScope]] = {}
    for scope in all_scopes:
        scopes_by_persona.setdefault(scope.persona_id, []).append(scope)

    active_scopes = scopes_by_persona.get(persona.id, [])
    accessible_team_ids = [scope.team_id for scope in active_scopes]
    accessible_teams = db.scalars(select(TeamContext).where(TeamContext.id.in_(accessible_team_ids))).all()

    return SessionResponse(
        active_persona=_persona_out(persona, active_scopes),
        personas=[_persona_out(item, scopes_by_persona.get(item.id, [])) for item in personas],
        accessible_teams=[_team_out(team) for team in accessible_teams],
    )


@router.get("/teams/{team_id}/overview", response_model=OverviewResponse)
def get_team_overview(team_id: str, persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)) -> OverviewResponse:
    team = require_team_access(team_id, persona, db)
    kpis = db.scalars(select(KpiSnapshot).where(KpiSnapshot.team_id == team_id)).all()
    alerts = db.scalars(select(AlertItem).where(AlertItem.team_id == team_id)).all()
    scenarios = db.scalars(select(ScenarioTemplate).where(ScenarioTemplate.team_id == team_id)).all()
    experiments = db.scalars(select(ExperimentRecord).where(ExperimentRecord.team_id == team_id)).all()
    tracks = db.scalars(select(TrainingTrack).where(TrainingTrack.team_id == team_id)).all()
    assets = db.scalars(select(KnowledgeAsset).where(KnowledgeAsset.team_id == team_id)).all()
    scale_candidates = [item for item in experiments if item.decision in {"scale", "pending"}]
    return OverviewResponse(
        team=_team_out(team),
        kpis=[_kpi_out(item) for item in kpis],
        alerts=[_alert_out(item) for item in alerts],
        scenarios=[_scenario_out(item) for item in scenarios],
        scale_candidates=[_experiment_out(item) for item in scale_candidates],
        training_tracks=[_track_out(item) for item in tracks],
        knowledge_assets=[_asset_out(item) for item in assets],
    )


@router.get("/teams/{team_id}/kpis", response_model=list[KpiMetricOut])
def get_team_kpis(team_id: str, persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)) -> list[KpiMetricOut]:
    require_team_access(team_id, persona, db)
    return [_kpi_out(item) for item in db.scalars(select(KpiSnapshot).where(KpiSnapshot.team_id == team_id)).all()]


@router.get("/teams/{team_id}/alerts", response_model=list[AlertItemOut])
def get_team_alerts(team_id: str, persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)) -> list[AlertItemOut]:
    require_team_access(team_id, persona, db)
    return [_alert_out(item) for item in db.scalars(select(AlertItem).where(AlertItem.team_id == team_id)).all()]


@router.get("/teams/{team_id}/scenarios", response_model=list[ScenarioTemplateOut])
def get_team_scenarios(team_id: str, persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)) -> list[ScenarioTemplateOut]:
    require_team_access(team_id, persona, db)
    return [_scenario_out(item) for item in db.scalars(select(ScenarioTemplate).where(ScenarioTemplate.team_id == team_id)).all()]


@router.get("/cases/{case_id}/context", response_model=CaseContextResponse)
def get_case_context(case_id: str, persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)) -> CaseContextResponse:
    case = db.get(CaseRecord, case_id)
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    require_team_access(case.team_id, persona, db)
    member = db.get(Member, case.member_id)
    policies = db.scalars(select(ProductPolicy).where(ProductPolicy.member_id == case.member_id)).all()
    interactions = db.scalars(select(InteractionEvent).where(InteractionEvent.case_id == case_id).order_by(InteractionEvent.occurred_at)).all()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return CaseContextResponse(
        case_record=CaseRecordOut(
            id=case.id,
            member_id=case.member_id,
            team=case.team_id,
            title=case.title,
            status=case.status,
            urgency=case.urgency,
            opened_at=case.opened_at,
            summary=case.summary,
            assigned_team=case.assigned_team,
            owner=case.owner,
        ),
        member=MemberProfileOut(
            id=member.id,
            full_name=member.full_name,
            segment=member.segment,
            membership_tier=member.membership_tier,
            postcode=member.postcode,
            vulnerability_flags=member.vulnerability_flags,
        ),
        product_policies=[
            ProductPolicyOut(
                id=policy.id,
                team=policy.team_id,
                product_name=policy.product_name,
                status=policy.status,
                renewal_date=policy.renewal_date,
                coverage_summary=policy.coverage_summary,
            )
            for policy in policies
        ],
        interactions=[
            InteractionEventOut(id=item.id, channel=item.channel, occurred_at=item.occurred_at, summary=item.summary)
            for item in interactions
        ],
    )


@router.get("/teams/{team_id}/experiments", response_model=list[ExperimentRecordOut])
def get_experiments(team_id: str, persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)) -> list[ExperimentRecordOut]:
    require_team_access(team_id, persona, db)
    return [_experiment_out(item) for item in db.scalars(select(ExperimentRecord).where(ExperimentRecord.team_id == team_id)).all()]


@router.get("/teams/{team_id}/governance", response_model=list[GovernanceReviewOut])
def get_governance(team_id: str, persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)) -> list[GovernanceReviewOut]:
    require_team_access(team_id, persona, db)
    return [_governance_out(item) for item in db.scalars(select(GovernanceReview).where(GovernanceReview.team_id == team_id)).all()]


@router.get("/teams/{team_id}/knowledge", response_model=list[KnowledgeAssetOut])
def get_knowledge(team_id: str, persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)) -> list[KnowledgeAssetOut]:
    require_team_access(team_id, persona, db)
    return [_asset_out(item) for item in db.scalars(select(KnowledgeAsset).where(KnowledgeAsset.team_id == team_id)).all()]


@router.get("/teams/{team_id}/academy", response_model=AcademyResponse)
def get_academy(team_id: str, persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)) -> AcademyResponse:
    team = require_team_access(team_id, persona, db)
    tracks = db.scalars(select(TrainingTrack).where(TrainingTrack.team_id == team_id)).all()
    return AcademyResponse(team=_team_out(team), training_tracks=[_track_out(item) for item in tracks])


@router.get("/teams/{team_id}/impact", response_model=ImpactResponse)
def get_impact(team_id: str, persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)) -> ImpactResponse:
    team = require_team_access(team_id, persona, db)
    kpis = db.scalars(select(KpiSnapshot).where(KpiSnapshot.team_id == team_id)).all()
    stories = db.scalars(select(ImpactStory).where(ImpactStory.team_id == team_id)).all()
    return ImpactResponse(
        team=_team_out(team),
        kpis=[_kpi_out(item) for item in kpis],
        stories=[ImpactStoryOut(id=item.id, team=item.team_id, title=item.title, baseline=item.baseline, current=item.current, evidence=item.evidence) for item in stories],
    )


@router.post("/copilot/runs", response_model=CopilotRunResult)
async def run_copilot(payload: CopilotRunRequest, persona: Persona = Depends(get_demo_persona), db: Session = Depends(get_db)):
    require_team_access(payload.team_id, persona, db)
    scenario = db.get(ScenarioTemplate, payload.scenario_id)
    case = db.get(CaseRecord, payload.case_id)
    if not scenario or scenario.team_id != payload.team_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found for team")
    if not case or case.team_id != payload.team_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found for team")

    scope = db.scalar(select(PermissionScope).where(PermissionScope.persona_id == persona.id, PermissionScope.team_id == payload.team_id))
    if not scope or not scope.can_run_copilot:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Persona cannot run copilot for this team")

    member = db.get(Member, case.member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found for case")
    policies = db.scalars(select(ProductPolicy).where(ProductPolicy.member_id == member.id)).all()
    assets = db.scalars(select(KnowledgeAsset).where(KnowledgeAsset.id.in_(scenario.linked_asset_ids))).all() if scenario.linked_asset_ids else []
    reviews = db.scalars(select(GovernanceReview).where(GovernanceReview.team_id == payload.team_id)).all()

    run_id = f"run-{uuid4().hex[:10]}"
    audit_event_id = f"audit-{uuid4().hex[:10]}"
    result = await create_copilot_result(
        db,
        user_input=payload.user_input,
        mode=payload.mode,
        case=case,
        member=member,
        policies=policies,
        scenario=scenario,
        reviews=reviews,
        assets=assets,
        run_id=run_id,
        audit_event_id=audit_event_id,
    )

    db.add(
        CopilotRun(
            id=run_id,
            persona_id=persona.id,
            team_id=payload.team_id,
            scenario_id=payload.scenario_id,
            case_id=payload.case_id,
            mode=payload.mode,
            user_input=payload.user_input,
            provider_used=result.provider_used,
            summary=result.summary,
            recommended_action=result.recommended_action,
            draft=result.draft,
            citations=[citation.model_dump() for citation in result.citations],
            risk_flags=[flag.model_dump() for flag in result.risk_flags],
            human_review_points=result.human_review_points,
        )
    )
    db.add(
        AuditEvent(
            id=audit_event_id,
            persona_id=persona.id,
            team_id=payload.team_id,
            entity_type="copilot_run",
            entity_id=run_id,
            action="run_created",
            detail=f"Copilot run created for scenario {payload.scenario_id} in {payload.mode} mode.",
        )
    )
    db.commit()
    return result


@router.post("/experiments/{experiment_id}/actions", response_model=ActionResponse)
def log_experiment_action(
    experiment_id: str,
    payload: ActionRequest,
    persona: Persona = Depends(get_demo_persona),
    db: Session = Depends(get_db),
) -> ActionResponse:
    experiment = db.get(ExperimentRecord, experiment_id)
    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")
    require_team_access(experiment.team_id, persona, db)
    audit_event_id = f"audit-{uuid4().hex[:10]}"
    db.add(
        AuditEvent(
            id=audit_event_id,
            persona_id=persona.id,
            team_id=experiment.team_id,
            entity_type="experiment",
            entity_id=experiment_id,
            action=payload.action,
            detail=payload.detail,
        )
    )
    db.commit()
    return ActionResponse(status="recorded", audit_event_id=audit_event_id)


@router.post("/governance/{review_id}/actions", response_model=ActionResponse)
def log_governance_action(
    review_id: str,
    payload: ActionRequest,
    persona: Persona = Depends(get_demo_persona),
    db: Session = Depends(get_db),
) -> ActionResponse:
    review = db.get(GovernanceReview, review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Governance review not found")
    require_team_access(review.team_id, persona, db)
    audit_event_id = f"audit-{uuid4().hex[:10]}"
    db.add(
        AuditEvent(
            id=audit_event_id,
            persona_id=persona.id,
            team_id=review.team_id,
            entity_type="governance_review",
            entity_id=review_id,
            action=payload.action,
            detail=payload.detail,
        )
    )
    db.commit()
    return ActionResponse(status="recorded", audit_event_id=audit_event_id)


@router.get("/audit-events", response_model=list[AuditEventOut])
def get_audit_events(
    team_id: str | None = Query(default=None),
    persona: Persona = Depends(get_demo_persona),
    db: Session = Depends(get_db),
) -> list[AuditEventOut]:
    if not persona.can_view_audit:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Persona cannot view audit events")
    statement = select(AuditEvent).order_by(desc(AuditEvent.created_at))
    if team_id:
        require_team_access(team_id, persona, db)
        statement = statement.where(AuditEvent.team_id == team_id)
    events = db.scalars(statement.limit(50)).all()
    return [
        AuditEventOut(
            id=item.id,
            persona_id=item.persona_id,
            team_id=item.team_id,
            entity_type=item.entity_type,
            entity_id=item.entity_id,
            action=item.action,
            detail=item.detail,
            created_at=item.created_at,
        )
        for item in events
    ]
