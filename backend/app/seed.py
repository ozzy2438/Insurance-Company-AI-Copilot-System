from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from .database import Base, engine
from .models import (
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


def reset_database(session: Session) -> None:
    for model in [
        AuditEvent,
        CopilotRun,
        ImpactStory,
        TrainingTrack,
        GovernanceReview,
        ExperimentRecord,
        ScenarioTemplate,
        KnowledgeAsset,
        InteractionEvent,
        CaseRecord,
        ProductPolicy,
        Member,
        AlertItem,
        KpiSnapshot,
        PermissionScope,
        Persona,
        TeamContext,
    ]:
        session.execute(delete(model))
    session.commit()


def ensure_schema() -> None:
    Base.metadata.create_all(bind=engine)


def seed_database(session: Session, *, reset: bool = False) -> None:
    ensure_schema()
    has_persona = session.scalar(select(Persona.id).limit(1))
    if has_persona and not reset:
        return

    if reset:
        reset_database(session)

    team_contexts = [
        TeamContext(
            id="roadside",
            label="Roadside Assistance",
            short_label="Roadside",
            strapline="High-pressure breakdown support with entitlement-aware guidance.",
            operating_goal="Reduce coordination time during member incidents without weakening dispatch controls.",
            lead="S. Mitchell",
            live_experiments=3,
            adoption_rate=71,
            governance_score=93,
        ),
        TeamContext(
            id="claims",
            label="Insurance & Claims",
            short_label="Claims",
            strapline="Structured first-contact support for policy and claims workflows.",
            operating_goal="Improve first-contact quality while keeping human review explicit for claim-sensitive decisions.",
            lead="R. Patel",
            live_experiments=2,
            adoption_rate=64,
            governance_score=89,
        ),
        TeamContext(
            id="contact-centre",
            label="Member Contact Centre",
            short_label="Contact Centre",
            strapline="Multi-product member support, repeat enquiry handling, and better handovers.",
            operating_goal="Give frontline teams faster access to context, approved language, and escalation patterns.",
            lead="L. Nguyen",
            live_experiments=4,
            adoption_rate=76,
            governance_score=91,
        ),
    ]
    session.add_all(team_contexts)

    personas = [
        Persona(
            id="transformation-lead",
            name="Avery Chen",
            title="Transformation Lead",
            description="Cross-functional sponsor with access across all operational teams and audit visibility.",
            default_team_id="roadside",
            can_view_audit=True,
        ),
        Persona(
            id="claims-manager",
            name="Rina Patel",
            title="Claims Operations Manager",
            description="Claims leader with governance review access and local copilot oversight.",
            default_team_id="claims",
            can_view_audit=False,
        ),
        Persona(
            id="frontline-coach",
            name="Jordan Lee",
            title="Frontline Enablement Coach",
            description="Supports roadside and contact centre prompting quality, adoption, and training routines.",
            default_team_id="contact-centre",
            can_view_audit=False,
        ),
    ]
    session.add_all(personas)
    session.add_all(
        [
            PermissionScope(persona_id="transformation-lead", team_id="roadside", can_review_governance=True, can_run_copilot=True),
            PermissionScope(persona_id="transformation-lead", team_id="claims", can_review_governance=True, can_run_copilot=True),
            PermissionScope(persona_id="transformation-lead", team_id="contact-centre", can_review_governance=True, can_run_copilot=True),
            PermissionScope(persona_id="claims-manager", team_id="claims", can_review_governance=True, can_run_copilot=True),
            PermissionScope(persona_id="frontline-coach", team_id="roadside", can_review_governance=False, can_run_copilot=True),
            PermissionScope(persona_id="frontline-coach", team_id="contact-centre", can_review_governance=False, can_run_copilot=True),
        ]
    )

    members = [
        Member(id="mem-roadside-001", full_name="James Holloway", segment="Roadside priority member", membership_tier="Premium Care", postcode="3000", vulnerability_flags=["dependent passenger"]),
        Member(id="mem-claims-001", full_name="Sonia Verma", segment="Home insurance member", membership_tier="Home Plus", postcode="3182", vulnerability_flags=["distressed claimant"]),
        Member(id="mem-contact-001", full_name="Michael D'Souza", segment="Multi-product member", membership_tier="Everyday Member", postcode="3051", vulnerability_flags=[]),
    ]
    session.add_all(members)
    session.add_all(
        [
            ProductPolicy(id="pol-road-001", member_id="mem-roadside-001", team_id="roadside", product_name="Roadside Premium Care", status="Active", renewal_date="2026-08-01", coverage_summary="Premium towing, accommodation support, and priority dispatch where eligible."),
            ProductPolicy(id="pol-claims-001", member_id="mem-claims-001", team_id="claims", product_name="Home Insurance Plus", status="Active", renewal_date="2026-11-14", coverage_summary="Home building and contents cover with emergency make-safe and escape of liquid review pathways."),
            ProductPolicy(id="pol-contact-001", member_id="mem-contact-001", team_id="contact-centre", product_name="Motor + Roadside Bundle", status="Active", renewal_date="2026-05-22", coverage_summary="Motor insurance, roadside, and service-plan billing support under one member profile."),
        ]
    )

    cases = [
        CaseRecord(id="case-roadside-001", member_id="mem-roadside-001", team_id="roadside", title="Night-time roadside battery failure", status="Open", urgency="High", opened_at="2026-03-10T19:41:00Z", summary="Vehicle disabled on a major arterial road at night with one dependent passenger in the car.", assigned_team="Roadside Assistance", owner="Night Dispatch Queue"),
        CaseRecord(id="case-claims-001", member_id="mem-claims-001", team_id="claims", title="Home water damage first-contact intake", status="In assessment", urgency="Medium", opened_at="2026-03-09T08:15:00Z", summary="Member reported sudden kitchen pipe burst with visible damage to flooring and cabinetry.", assigned_team="Claims Intake", owner="Claims Intake Pilot Cohort"),
        CaseRecord(id="case-contact-001", member_id="mem-contact-001", team_id="contact-centre", title="Repeat enquiry on unresolved billing issue", status="Escalation pending", urgency="Medium", opened_at="2026-03-08T11:20:00Z", summary="Member has contacted the centre three times regarding the same unresolved billing and fulfilment mismatch.", assigned_team="Member Contact Centre", owner="Member Support Resolution Desk"),
    ]
    session.add_all(cases)
    session.add_all(
        [
            InteractionEvent(case_id="case-roadside-001", channel="Phone", occurred_at="2026-03-10T19:41:00Z", summary="Member reported flat battery and unsafe roadside position."),
            InteractionEvent(case_id="case-roadside-001", channel="Agent note", occurred_at="2026-03-10T19:46:00Z", summary="Priority dispatch flagged due to dependent passenger and traffic exposure."),
            InteractionEvent(case_id="case-claims-001", channel="Phone", occurred_at="2026-03-09T08:15:00Z", summary="Member reported kitchen pipe burst and immediate damage to cabinets and flooring."),
            InteractionEvent(case_id="case-claims-001", channel="Case note", occurred_at="2026-03-09T08:29:00Z", summary="Explained assessor review path and required make-safe evidence."),
            InteractionEvent(case_id="case-contact-001", channel="Phone", occurred_at="2026-03-08T11:20:00Z", summary="Member reported third unresolved contact regarding billing ownership."),
            InteractionEvent(case_id="case-contact-001", channel="Email", occurred_at="2026-03-09T07:05:00Z", summary="Member requested a single contact point and confirmed frustration with repeated transfers."),
        ]
    )

    knowledge_assets = [
        KnowledgeAsset(id="asset-roadside-summary", team_id="roadside", type="prompt", title="Member situation summary prompt", description="Approved prompt for context compression before dispatch or escalation.", owner="S. Mitchell", status="approved", tags=["summary", "dispatch", "frontline"], usage_count=248, rating=4.8, excerpt="Summarise the current member situation, entitlements, and any active risks in under 100 words."),
        KnowledgeAsset(id="asset-roadside-playbook", team_id="roadside", type="playbook", title="Unsafe roadside escalation playbook", description="Reference pack for high-risk incidents and priority dispatch decisions.", owner="A. Kumar", status="approved", tags=["safety", "escalation", "playbook"], usage_count=94, rating=4.6, excerpt="Escalate immediately when exposure risk, vulnerable passengers, or prolonged unsafe wait conditions are present."),
        KnowledgeAsset(id="asset-claims-policy", team_id="claims", type="policy", title="First-contact policy navigator pack", description="Claims policy reference bundle aligned to intake use cases.", owner="R. Patel", status="approved", tags=["claims", "policy", "coverage"], usage_count=181, rating=4.9, excerpt="Use reviewable language. Surface likely policy areas, required evidence, and the next assessor-led step."),
        KnowledgeAsset(id="asset-claims-checklist", team_id="claims", type="workflow", title="Home water damage document checklist", description="Reusable checklist for evidence capture and make-safe steps.", owner="E. Saunders", status="draft", tags=["checklist", "home", "water-damage"], usage_count=52, rating=4.2, excerpt="Ask for incident timing, damage photos, emergency make-safe receipts, and any prior maintenance notes."),
        KnowledgeAsset(id="asset-contact-handover", team_id="contact-centre", type="prompt", title="Structured handover note generator", description="Approved handover format for unresolved multi-team service issues.", owner="L. Nguyen", status="approved", tags=["handover", "case-note", "repeat-contact"], usage_count=312, rating=4.8, excerpt="Summarise member ask, actions taken, unresolved blocker, accountable team, and the next contact commitment."),
        KnowledgeAsset(id="asset-contact-repeat", team_id="contact-centre", type="playbook", title="Repeat enquiry resolution guide", description="Pattern library for diagnosing ownership gaps and repeat-contact drivers.", owner="P. Zhao", status="approved", tags=["resolution", "root-cause", "contact-centre"], usage_count=149, rating=4.7, excerpt="Use a single-owner model when two or more teams have already touched the case without closure."),
        KnowledgeAsset(id="asset-academy-manager", team_id="contact-centre", type="copilot-studio", title="Manager coaching starter kit", description="Coaching assets for team leaders running prompt quality sessions.", owner="P. Zhao", status="approved", tags=["academy", "manager", "coaching"], usage_count=34, rating=4.5, excerpt="Includes session flow, scorecards, and safe-use reminders for first-line leaders."),
    ]
    session.add_all(knowledge_assets)

    scenarios = [
        ScenarioTemplate(id="scenario-roadside-breakdown", team_id="roadside", case_id="case-roadside-001", title="Critical roadside breakdown triage", member_moment="Night-time breakdown on a major arterial road", summary="The agent needs a fast situation summary, entitlement view, and a safe next action recommendation.", objective="Reduce coordination delay while surfacing any safety and entitlement exceptions.", recommended_prompt="Summarise the member situation, current roadside status, entitlements, and the next recommended action. Keep human review points explicit.", human_review_points=["Confirm exact member location before dispatch escalation.", "Validate any premium towing or accommodation entitlement before communication.", "Escalate if incident involves vulnerable passengers or unsafe roadside conditions."], references=[{"title": "Roadside escalation playbook", "type": "playbook", "detail": "Emergency traffic exposure and vulnerable passenger handling."}, {"title": "Member entitlement matrix", "type": "policy", "detail": "Premium towing and after-hours limits."}, {"title": "Dispatch coordination guide", "type": "guide", "detail": "Expected wait-time scripting and escalation triggers."}], draft_output=["Member is stranded on a high-risk roadside corridor with one dependent passenger and an active premium assistance entitlement.", "Current case history shows one inbound contact, no open roadside incidents, and no prior dispatch duplication.", "Recommended next step: confirm exact pin location, lock a priority dispatch, then provide a time-bound verbal update with escalation wording if ETA exceeds threshold."], canned_conversation=[{"role": "assistant", "content": "Roadside workspace ready. I can summarise the incident, surface entitlements, and draft the next communication."}, {"role": "user", "content": "The member is on CityLink with a flat battery and a child in the vehicle. What should the agent do next?"}, {"role": "assistant", "content": "Prioritise location confirmation and safety status first, then move the case into priority dispatch. Keep entitlement guidance visible, but have the agent confirm premium cover before quoting any secondary towing option."}], linked_asset_ids=["asset-roadside-summary", "asset-roadside-playbook"]),
        ScenarioTemplate(id="scenario-claims-intake", team_id="claims", case_id="case-claims-001", title="Home water damage first-contact intake", member_moment="A distressed member needs clarity on coverage, documents, and next steps.", summary="The agent needs structured intake support and policy-grounded drafting without making a binding claim decision.", objective="Improve first-contact quality and keep human review explicit for any claims interpretation.", recommended_prompt="Summarise the reported loss, list the likely policy areas to review, and draft a member-safe explanation of next steps without implying claim approval.", human_review_points=["Do not state that the claim is approved or declined.", "Ensure any exclusions or limitations are described as items for assessor review.", "Confirm the member receives the documentation checklist before ending the contact."], references=[{"title": "Home claims first-contact playbook", "type": "playbook", "detail": "Mandatory intake questions and vulnerability markers."}, {"title": "Water ingress coverage guide", "type": "policy", "detail": "Escape of liquid, gradual damage, and emergency make-safe wording."}, {"title": "Claims empathy response pack", "type": "guide", "detail": "Approved language for distressed-member communications."}], draft_output=["Reported issue: sudden kitchen pipe burst with visible water damage to cabinetry and flooring.", "Likely policy review areas: escape of liquid, emergency make-safe, temporary accommodation triggers, and any pre-existing damage considerations.", "Draft member message: explain that the claim will be assessed, outline the document list, and confirm the next claims contact point without implying final coverage."], canned_conversation=[{"role": "assistant", "content": "Claims workspace ready. I can structure intake, surface policy references, and help draft the next-step summary."}, {"role": "user", "content": "Can the agent say this water damage is covered?"}, {"role": "assistant", "content": "No. The agent should explain that the incident appears to fall within a reviewable coverage pathway, but final coverage must be confirmed after policy and evidence assessment."}], linked_asset_ids=["asset-claims-policy", "asset-claims-checklist"]),
        ScenarioTemplate(id="scenario-contact-repeat", team_id="contact-centre", case_id="case-contact-001", title="Repeat enquiry resolution planning", member_moment="A member has contacted the centre three times about the same unresolved service issue.", summary="The agent needs a joined-up member view, a concise root-cause summary, and a cleaner handover path.", objective="Reduce repeat contact while improving resolution confidence and note quality.", recommended_prompt="Summarise the repeated enquiry history, identify the unresolved blocker, and draft a clear ownership handover with next contact commitment.", human_review_points=["Confirm all open service requests before promising a resolution date.", "Check whether any complaint handling obligations are triggered.", "Ensure the drafted handover note reflects the actual owner team."], references=[{"title": "Repeat enquiry resolution guide", "type": "playbook", "detail": "How to identify ownership breakdowns and duplicate work."}, {"title": "Complaint threshold process", "type": "policy", "detail": "Escalation wording and obligations once threshold is crossed."}, {"title": "Case-note quality standard", "type": "guide", "detail": "Mandatory structure for follow-up notes and next-contact promises."}], draft_output=["The member has made three contacts in six days, all linked to the same unresolved billing service request.", "The current blocker is unclear ownership between billing operations and service fulfilment.", "Recommended next step: issue a single owner handover, confirm expected contact time, and record the root-cause summary in the case note."], canned_conversation=[{"role": "assistant", "content": "Contact centre workspace ready. I can build a member overview, identify repeat-contact patterns, and draft a cleaner escalation note."}, {"role": "user", "content": "Show me the best way to hand this over without another bounce between teams."}, {"role": "assistant", "content": "Use a single-owner handover with the unresolved blocker, prior actions, and next contact promise in one note. Avoid open-ended wording that leaves ownership ambiguous."}], linked_asset_ids=["asset-contact-handover", "asset-contact-repeat"]),
    ]
    session.add_all(scenarios)

    experiments = [
        ExperimentRecord(id="exp-roadside-summary", team_id="roadside", name="Roadside Member Context Summariser", owner="S. Mitchell", stage="completed", risk="low", target_metric="Average handle time", baseline="11.2 mins", pilot_result="9.4 mins", decision="scale", summary="Context summaries reduced the time agents spent assembling case history before dispatch decisions.", dependencies=["Knowledge pack approved", "Dispatch supervisor buy-in confirmed"], linked_governance_ids=["gov-roadside-hitl"], linked_knowledge_ids=["asset-roadside-summary", "asset-roadside-playbook"], timeline=[{"date": "2026-01-14", "label": "Pilot launched", "detail": "12 roadside team leaders onboarded."}, {"date": "2026-02-04", "label": "Mid-point review", "detail": "AHT tracking exceeded target trend line."}, {"date": "2026-02-28", "label": "Scale decision proposed", "detail": "Ready for shift-wide rollout pack."}]),
        ExperimentRecord(id="exp-claims-policy", team_id="claims", name="Claims First Contact Policy Navigator", owner="R. Patel", stage="in-flight", risk="medium", target_metric="First-contact resolution", baseline="67%", pilot_result="73%", decision="pending", summary="Structured policy guidance is lifting intake quality, but privacy renewal and source traceability work remain open.", dependencies=["Privacy renewal", "Source citation pattern uplift"], linked_governance_ids=["gov-claims-privacy", "gov-claims-hitl"], linked_knowledge_ids=["asset-claims-policy", "asset-claims-checklist"], timeline=[{"date": "2026-01-08", "label": "Use case approved", "detail": "Pilot approved with human review controls."}, {"date": "2026-02-12", "label": "Pilot cohort active", "detail": "12 agents using navigator in first-contact flow."}, {"date": "2026-03-06", "label": "Governance hold point", "detail": "Awaiting privacy renewal sign-off."}]),
        ExperimentRecord(id="exp-contact-handover", team_id="contact-centre", name="Handover Drafting Assistant", owner="L. Nguyen", stage="in-flight", risk="low", target_metric="Admin effort", baseline="7.1 mins", pilot_result="5.6 mins", decision="iterate", summary="The team is seeing strong time savings, but escalation wording needs tighter complaint-threshold handling.", dependencies=["Complaint wording update", "Team leader coaching"], linked_governance_ids=["gov-contact-complaints"], linked_knowledge_ids=["asset-contact-handover", "asset-contact-repeat"], timeline=[{"date": "2026-01-20", "label": "Pilot launched", "detail": "Contact centre leaders selected repeat-enquiry cohort."}, {"date": "2026-02-18", "label": "Content refinement", "detail": "Handover templates adjusted for complaint thresholds."}, {"date": "2026-03-05", "label": "Iteration decision", "detail": "Ready for second-round quality check."}]),
        ExperimentRecord(id="exp-governance-coach", team_id="contact-centre", name="Prompt Coach for Team Leaders", owner="P. Zhao", stage="pipeline", risk="low", target_metric="Approved prompt reuse", baseline="62%", pilot_result="Not started", decision="pending", summary="A coaching-focused agent to reduce poor prompt patterns before they hit frontline usage.", dependencies=["Champion coverage uplift", "Prompt scorecard alignment"], linked_governance_ids=["gov-coach-lowrisk"], linked_knowledge_ids=["asset-academy-manager"], timeline=[{"date": "2026-03-01", "label": "Opportunity logged", "detail": "Selected as next capability after contact centre uplift."}]),
    ]
    session.add_all(experiments)

    governance_reviews = [
        GovernanceReview(id="gov-roadside-hitl", team_id="roadside", title="Roadside dispatch human-in-the-loop control", owner="A. Kumar", risk="low", status="approved", due_date="2026-06-30", controls=["Dispatch recommendation must be confirmed by the agent before booking.", "Unsafe location triggers remain mandatory and cannot be bypassed by AI output.", "Entitlement exceptions require supervisor review."], exceptions=[], linked_experiment_ids=["exp-roadside-summary"]),
        GovernanceReview(id="gov-claims-privacy", team_id="claims", title="Claims data handling renewal", owner="E. Saunders", risk="high", status="renewal-due", due_date="2026-03-14", controls=["No claims output is shown without source traceability.", "Sensitive claim information remains restricted to approved pilot cohort."], exceptions=["Renewal approval due before pilot expansion beyond cohort."], linked_experiment_ids=["exp-claims-policy"]),
        GovernanceReview(id="gov-claims-hitl", team_id="claims", title="Claims decision boundary review", owner="R. Patel", risk="high", status="review", due_date="2026-03-20", controls=["No binding coverage statements allowed in generated outputs.", "Draft communication must include assessor-review language.", "Claims approval decisions remain outside scope."], exceptions=["Source citation wording needs final legal review."], linked_experiment_ids=["exp-claims-policy"]),
        GovernanceReview(id="gov-contact-complaints", team_id="contact-centre", title="Complaint threshold escalation wording", owner="L. Nguyen", risk="medium", status="review", due_date="2026-03-19", controls=["Complaint threshold prompts must surface formal complaint obligations.", "Handover notes must identify final accountable team."], exceptions=["Need updated wording pack for complaint-adjacent scenarios."], linked_experiment_ids=["exp-contact-handover"]),
        GovernanceReview(id="gov-coach-lowrisk", team_id="contact-centre", title="Prompt coaching low-risk content review", owner="P. Zhao", risk="low", status="approved", due_date="2026-07-01", controls=["Training content can be reused across operational teams once approved."], exceptions=[], linked_experiment_ids=["exp-governance-coach"]),
    ]
    session.add_all(governance_reviews)

    training_tracks = [
        TrainingTrack(id="track-roadside-frontline", team_id="roadside", title="Roadside frontline copilot onboarding", audience="Frontline agents", owner="S. Mitchell", completion=84, status="on-track", next_session="2026-03-17", modules=["Prompt basics", "Entitlement-safe summarisation", "Escalation boundaries"]),
        TrainingTrack(id="track-claims-leads", team_id="claims", title="Claims leaders governance coaching", audience="Team leaders", owner="R. Patel", completion=68, status="at-risk", next_session="2026-03-18", modules=["Human review boundaries", "Traceable draft outputs", "Risk escalation obligations"]),
        TrainingTrack(id="track-contact-champions", team_id="contact-centre", title="Contact centre AI champions network", audience="Champions and coaches", owner="P. Zhao", completion=57, status="at-risk", next_session="2026-03-15", modules=["Champion toolkit", "Prompt scorecards", "Manager coaching rhythm"]),
        TrainingTrack(id="track-contact-frontline", team_id="contact-centre", title="Member support prompting essentials", audience="Frontline agents", owner="L. Nguyen", completion=89, status="completed", next_session="2026-04-03", modules=["Repeat enquiry handling", "Case note quality", "Complaint threshold escalation"]),
    ]
    session.add_all(training_tracks)

    alerts = [
        AlertItem(id="claims-renewal", team_id="claims", severity="warning", title="Claims privacy renewal due this week", body="Renew the data-handling approval for the First Contact Policy Navigator before pilot expansion.", route="/governance?team=claims&review=gov-claims-privacy"),
        AlertItem(id="roadside-scale", team_id="roadside", severity="info", title="Roadside summariser ready for scale decision", body="Impact evidence now exceeds the agreed AHT threshold and agent satisfaction target.", route="/experiments?team=roadside&experiment=exp-roadside-summary"),
        AlertItem(id="contact-academy", team_id="contact-centre", severity="critical", title="Champion coverage is below target in contact centre", body="Two new team leaders still need the enablement and governance coaching path.", route="/academy?team=contact-centre"),
    ]
    session.add_all(alerts)

    kpis = [
        KpiSnapshot(id="roadside-adoption", team_id="roadside", label="Copilot adoption", value="71%", change="+11%", direction="up", target="75%", note="Shift leaders have completed the prompting uplift pack."),
        KpiSnapshot(id="roadside-aht", team_id="roadside", label="Average handle time", value="-16%", change="+4%", direction="up", target="-18%", note="Driven by faster entitlement checks and handover summaries."),
        KpiSnapshot(id="claims-fcr", team_id="claims", label="First-contact resolution", value="73%", change="+6%", direction="up", target="76%", note="Policy navigator usage is strongest in motor and home claims intake."),
        KpiSnapshot(id="claims-exceptions", team_id="claims", label="Compliance exceptions", value="2", change="-1", direction="up", target="0", note="Remaining exceptions are privacy renewal follow-ups."),
        KpiSnapshot(id="contact-admin", team_id="contact-centre", label="Admin effort", value="-21%", change="+5%", direction="up", target="-24%", note="Case-note automation and handover drafting are the main levers."),
        KpiSnapshot(id="contact-reuse", team_id="contact-centre", label="Approved prompt reuse", value="82%", change="+9%", direction="up", target="85%", note="Prompt library is now part of team leader coaching sessions."),
    ]
    session.add_all(kpis)

    session.add_all(
        [
            ImpactStory(id="impact-roadside", team_id="roadside", title="Roadside context compression reduced coordination lag", baseline="Average handle time: 11.2 mins", current="Average handle time: 9.4 mins", evidence=["Dispatch prep time reduced by 1.8 minutes in pilot cohort.", "Agent confidence score improved from 3.6 to 4.4 out of 5.", "Escalation quality scores improved during high-risk cases."]),
            ImpactStory(id="impact-claims", team_id="claims", title="Claims intake quality improved without widening decision risk", baseline="First-contact resolution: 67%", current="First-contact resolution: 73%", evidence=["Policy reference consistency increased across pilot cohort.", "No pilot outputs crossed the claim approval boundary.", "Remaining blocker is privacy renewal, not operational value."]),
            ImpactStory(id="impact-contact", team_id="contact-centre", title="Handover drafting reduced repeat admin effort", baseline="After-call work: 7.1 mins", current="After-call work: 5.6 mins", evidence=["Handover completeness improved across multi-team cases.", "Prompt reuse increased as approved templates spread via team leaders.", "Complaint-threshold language still needs refinement before scale."]),
        ]
    )
    session.commit()
