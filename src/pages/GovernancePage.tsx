import { useSearchParams } from 'react-router-dom';
import { useState } from 'react';
import { useAppState, useRouteTeam } from '../app-state';
import { api } from '../api/client';
import { DetailDrawer, EmptyState, ErrorState, LoadingState, PageHero, Panel, ToneBadge } from '../components';
import { useApiResource } from '../hooks/useApiResource';

export function GovernancePage() {
  const team = useRouteTeam();
  const { session, selectedPersonaId } = useAppState();
  const [searchParams, setSearchParams] = useSearchParams();
  const [actionMessage, setActionMessage] = useState<string | null>(null);
  const governanceState = useApiResource(() => api.getGovernance(team, selectedPersonaId), [team, selectedPersonaId]);
  const reviews = governanceState.data ?? [];
  const selected = reviews.find((item) => item.id === searchParams.get('review'));
  const canReviewGovernance =
    session?.activePersona.permissionScopes.some((scope) => scope.teamId === team && scope.canReviewGovernance) ?? false;

  if (governanceState.loading && !reviews.length) {
    return <LoadingState title="Loading governance reviews" body="Fetching risk, control, and approval data from the backend." />;
  }

  if (governanceState.error && !reviews.length) {
    return <ErrorState title="Governance unavailable" body={governanceState.error} />;
  }

  async function logGovernanceAction(action: string, detail: string) {
    if (!selected) {
      return;
    }
    try {
      const result = await api.createGovernanceAction(selected.id, action, detail, selectedPersonaId);
      setActionMessage(`Governance action recorded under audit event ${result.auditEventId}.`);
    } catch (error: unknown) {
      setActionMessage(error instanceof Error ? error.message : 'Unable to record governance action.');
    }
  }

  return (
    <div className="page-stack">
      <PageHero
        eyebrow="Responsible AI"
        title="Governance and risk"
        description="A visible operating layer for risk classification, approvals, privacy status, and explicit human review control points."
      />

      <div className="page-grid two-up">
        <Panel title="Control posture" subtitle="Governance is part of delivery, not a final checkpoint.">
          <div className="stack">
            <div className="row-stat"><span>Approved reviews</span><strong>{reviews.filter((item) => item.status === 'approved').length}</strong></div>
            <div className="row-stat"><span>Renewal due</span><strong>{reviews.filter((item) => item.status === 'renewal-due').length}</strong></div>
            <div className="row-stat"><span>Under review</span><strong>{reviews.filter((item) => item.status === 'review').length}</strong></div>
          </div>
        </Panel>

        <Panel title="Guardrail themes" subtitle="The recurring design boundaries across member-service use cases.">
          <ul className="simple-list">
            <li>No binding customer decisions are delegated to AI.</li>
            <li>Claims-sensitive outputs must keep review and source language explicit.</li>
            <li>Workflow speed gains cannot bypass escalation triggers or privacy obligations.</li>
          </ul>
        </Panel>
      </div>

      <Panel title="Review board" subtitle="Open and approved controls linked directly to experiments.">
        {reviews.length ? (
          <div className="stack">
            {reviews.map((review) => (
              <button
                key={review.id}
                className="governance-card"
                onClick={() => {
                  const next = new URLSearchParams(searchParams);
                  next.set('team', team);
                  next.set('review', review.id);
                  setSearchParams(next);
                }}
                type="button"
              >
                <div className="row-link-head">
                  <strong>{review.title}</strong>
                  <ToneBadge
                    tone={
                      review.status === 'approved'
                        ? 'positive'
                        : review.status === 'renewal-due'
                          ? 'warning'
                          : review.status === 'blocked'
                            ? 'critical'
                            : 'info'
                    }
                  >
                    {review.status}
                  </ToneBadge>
                </div>
                <p>Owner: {review.owner} · Due: {review.dueDate}</p>
                <div className="badge-row">
                  <ToneBadge tone={review.risk === 'high' ? 'critical' : review.risk === 'medium' ? 'warning' : 'calm'}>
                    {review.risk} risk
                  </ToneBadge>
                  <span>{review.linkedExperimentIds.length} linked experiments</span>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <EmptyState title="No governance reviews" body="This team does not yet have any governance reviews in the backend sandbox." />
        )}
      </Panel>

      {selected ? (
        <DetailDrawer
          title={selected.title}
          subtitle={`${selected.owner} · due ${selected.dueDate}`}
          onClose={() => {
            const next = new URLSearchParams(searchParams);
            next.delete('review');
            next.set('team', team);
            setSearchParams(next);
          }}
        >
          <div className="stack">
            {actionMessage ? <div className="info-block"><strong>Audit note</strong><p>{actionMessage}</p></div> : null}
            <div className="info-block">
              <strong>Controls</strong>
              <ul className="simple-list">
                {selected.controls.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="info-block">
              <strong>Exceptions and follow-ups</strong>
              <ul className="simple-list">
                {selected.exceptions.length ? selected.exceptions.map((item) => <li key={item}>{item}</li>) : <li>No open exceptions.</li>}
              </ul>
            </div>
            {canReviewGovernance ? (
              <div className="badge-row">
                <button
                  className="primary-button"
                  onClick={() =>
                    logGovernanceAction(
                      'control_review_logged',
                      `Control review logged for ${selected.title}; current status ${selected.status}.`
                    )
                  }
                  type="button"
                >
                  Record control review
                </button>
                <button
                  className="ghost-button"
                  onClick={() =>
                    logGovernanceAction(
                      'follow_up_requested',
                      `Follow-up requested for ${selected.title}; due date ${selected.dueDate}.`
                    )
                  }
                  type="button"
                >
                  Log follow-up
                </button>
              </div>
            ) : (
              <div className="info-block">
                <strong>Review permissions</strong>
                <p>This demo persona can view governance status but cannot record governance review actions for this team.</p>
              </div>
            )}
          </div>
        </DetailDrawer>
      ) : null}
    </div>
  );
}
