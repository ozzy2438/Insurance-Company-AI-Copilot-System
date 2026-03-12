from __future__ import annotations

from collections.abc import Sequence

import httpx
from sqlalchemy.orm import Session

from ..config import OLLAMA_BASE_URL, OLLAMA_MODEL
from ..models import CaseRecord, GovernanceReview, KnowledgeAsset, Member, ProductPolicy, ScenarioTemplate
from ..schemas import CitationOut, CopilotRunResult, RiskFlagOut


def _build_summary(member: Member, case: CaseRecord, policies: Sequence[ProductPolicy]) -> str:
    products = ", ".join(policy.product_name for policy in policies)
    vulnerability = ", ".join(member.vulnerability_flags) if member.vulnerability_flags else "no flagged vulnerabilities"
    return (
        f"{member.full_name} is in a {case.urgency.lower()}-urgency {case.team_id} workflow with {products}. "
        f"Current case summary: {case.summary} Member tier: {member.membership_tier}; risk modifiers: {vulnerability}."
    )


def _build_recommended_action(case: CaseRecord, scenario: ScenarioTemplate, reviews: Sequence[GovernanceReview]) -> str:
    review_cautions = [review.title for review in reviews if review.status in {"review", "renewal-due"}]
    if review_cautions:
        caution_text = f" Keep open review items visible: {', '.join(review_cautions)}."
    else:
        caution_text = ""

    return (
        f"Use the '{scenario.title}' workflow to guide the next step, validate the accountable owner in {case.assigned_team}, "
        f"and keep human review explicit before any member-facing commitment.{caution_text}"
    )


def _build_draft(case: CaseRecord, scenario: ScenarioTemplate) -> str:
    return " ".join(scenario.draft_output[:2]) + f" Draft for agent review: {scenario.draft_output[-1]}"


def _build_citations(scenario: ScenarioTemplate, assets: Sequence[KnowledgeAsset], policies: Sequence[ProductPolicy]) -> list[CitationOut]:
    citations = [CitationOut(title=item["title"], type=item["type"], detail=item["detail"]) for item in scenario.references]
    for asset in assets:
        citations.append(CitationOut(title=asset.title, type=asset.type, detail=asset.excerpt))
    for policy in policies:
        citations.append(CitationOut(title=policy.product_name, type="policy-product", detail=policy.coverage_summary))
    seen: set[tuple[str, str]] = set()
    unique: list[CitationOut] = []
    for citation in citations:
        key = (citation.title, citation.detail)
        if key not in seen:
            seen.add(key)
            unique.append(citation)
    return unique[:6]


def _build_risk_flags(member: Member, reviews: Sequence[GovernanceReview]) -> list[RiskFlagOut]:
    flags: list[RiskFlagOut] = []
    for item in member.vulnerability_flags:
        flags.append(RiskFlagOut(level="context", text=f"Member context flag: {item}"))
    for review in reviews:
        if review.status in {"review", "renewal-due"}:
            flags.append(RiskFlagOut(level=review.risk, text=f"Governance follow-up: {review.title} ({review.status})"))
    return flags[:5]


def _build_human_review_points(scenario: ScenarioTemplate, reviews: Sequence[GovernanceReview]) -> list[str]:
    points = list(scenario.human_review_points)
    for review in reviews:
        points.extend(review.exceptions)
    deduped: list[str] = []
    for point in points:
        if point and point not in deduped:
            deduped.append(point)
    return deduped[:6]


def _build_live_draft(user_input: str, summary: str, recommended_action: str) -> str:
    return (
        "Provide a concise operational draft for an internal frontline agent. "
        "Keep it actionable, highlight the next step, and avoid making binding customer decisions.\n\n"
        f"Case summary:\n{summary}\n\nRecommended action:\n{recommended_action}\n\nUser request:\n{user_input}"
    )


async def _maybe_generate_live_draft(prompt: str) -> str | None:
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": OLLAMA_MODEL,
                    "stream": False,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a safe internal operations copilot. Be concise and do not make final decisions.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                },
            )
            response.raise_for_status()
            payload = response.json()
            return payload.get("message", {}).get("content")
    except Exception:
        return None


async def create_copilot_result(
    db: Session,
    *,
    user_input: str,
    mode: str,
    case: CaseRecord,
    member: Member,
    policies: Sequence[ProductPolicy],
    scenario: ScenarioTemplate,
    reviews: Sequence[GovernanceReview],
    assets: Sequence[KnowledgeAsset],
    run_id: str,
    audit_event_id: str,
) -> CopilotRunResult:
    summary = _build_summary(member, case, policies)
    recommended_action = _build_recommended_action(case, scenario, reviews)
    draft = _build_draft(case, scenario)
    provider_used = "synthetic-orchestrator"

    if mode == "live":
        live_prompt = _build_live_draft(user_input, summary, recommended_action)
        live_draft = await _maybe_generate_live_draft(live_prompt)
        if live_draft:
            draft = live_draft
            provider_used = "ollama-live"

    return CopilotRunResult(
        run_id=run_id,
        audit_event_id=audit_event_id,
        provider_used=provider_used,
        summary=summary,
        recommended_action=recommended_action,
        draft=draft,
        citations=_build_citations(scenario, assets, policies),
        risk_flags=_build_risk_flags(member, reviews),
        human_review_points=_build_human_review_points(scenario, reviews),
    )
