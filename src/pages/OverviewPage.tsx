import { Link } from 'react-router-dom';
import { useAppState, useRouteTeam } from '../app-state';
import { api } from '../api/client';
import { EmptyState, ErrorState, LoadingState, MetricCard, PageHero, Panel, ToneBadge } from '../components';
import { useApiResource } from '../hooks/useApiResource';

export function OverviewPage() {
  const team = useRouteTeam();
  const { session, selectedPersonaId } = useAppState();
  const overviewState = useApiResource(() => api.getOverview(team, selectedPersonaId), [team, selectedPersonaId]);
  const canViewAudit = session?.activePersona.canViewAudit ?? false;
  const auditState = useApiResource(
    () => (canViewAudit ? api.getAuditEvents(selectedPersonaId, team) : Promise.resolve([])),
    [canViewAudit, selectedPersonaId, team]
  );

  if (overviewState.loading && !overviewState.data) {
    return <LoadingState title="Loading operating pulse" body="Fetching adoption, experiment, governance, and enablement signals from the backend." />;
  }

  if (overviewState.error && !overviewState.data) {
    return <ErrorState title="Overview unavailable" body={overviewState.error} />;
  }

  const overview = overviewState.data;
  if (!overview) {
    return <EmptyState title="No overview data" body="The selected team does not yet have a backend-backed overview payload." />;
  }

  const context = overview.team;
  const metrics = overview.kpis;
  const alerts = overview.alerts;
  const assets = overview.knowledgeAssets;
  const tracks = overview.trainingTracks;
  const scenarios = overview.scenarios;
  const scaleCandidates = overview.scaleCandidates;
  const auditEvents = auditState.data ?? [];

  return (
    <div className="page-stack">
      <PageHero
        eyebrow="Executive view"
        title={`${context.shortLabel} transformation pulse`}
        description="A single operating view across adoption, experiment readiness, governance health, and frontline enablement."
        action={
          <div className="hero-chip-grid">
            <div className="hero-chip">
              <span>Lead</span>
              <strong>{context.lead}</strong>
            </div>
            <div className="hero-chip">
              <span>Adoption</span>
              <strong>{context.adoptionRate}%</strong>
            </div>
            <div className="hero-chip">
              <span>Governance</span>
              <strong>{context.governanceScore}/100</strong>
            </div>
          </div>
        }
      />

      <div className="metric-grid">
        {metrics.map((metric) => (
          <MetricCard
            key={metric.id}
            label={metric.label}
            value={metric.value}
            change={metric.change}
            note={metric.note}
          />
        ))}
      </div>

      {overviewState.error && overviewState.data ? (
        <ErrorState title="Overview refresh issue" body={overviewState.error} compact />
      ) : null}

      <div className="page-grid two-up">
        <Panel title="Operating narrative" subtitle="Why this team context matters right now.">
          <div className="narrative-block">
            <p>{context.operatingGoal}</p>
            <div className="badge-row">
              <ToneBadge tone="info">{context.liveExperiments} active experiments</ToneBadge>
              <ToneBadge tone="positive">{assets.filter((item) => item.status === 'approved').length} approved assets</ToneBadge>
              <ToneBadge tone={tracks.some((item) => item.status === 'at-risk') ? 'warning' : 'positive'}>
                {tracks.filter((item) => item.status === 'at-risk').length} enablement risks
              </ToneBadge>
            </div>
            <div className="insight-list">
              <div>
                <strong>Frontline outcomes</strong>
                <p>Operational copilots are scoped to reduce friction inside service interactions, not replace judgment.</p>
              </div>
              <div>
                <strong>Governance posture</strong>
                <p>Every AI use case is linked to a review status, controls, and explicit human review checkpoints.</p>
              </div>
              <div>
                <strong>Adoption path</strong>
                <p>Training, approved prompts, and champion coverage are treated as part of the product, not change-management afterthoughts.</p>
              </div>
            </div>
          </div>
        </Panel>

        <Panel title="Action queue" subtitle="Signals requiring leadership attention.">
          {alerts.length ? (
            <div className="stack">
              {alerts.map((alert) => (
                <Link key={alert.id} to={alert.route} className="row-link-card">
                  <div className="row-link-head">
                    <strong>{alert.title}</strong>
                    <ToneBadge tone={alert.severity === 'critical' ? 'critical' : alert.severity === 'warning' ? 'warning' : 'info'}>
                      {alert.severity}
                    </ToneBadge>
                  </div>
                  <p>{alert.body}</p>
                </Link>
              ))}
            </div>
          ) : (
            <EmptyState title="No active alerts" body="This team currently has no unresolved alerts in the attention queue." />
          )}
        </Panel>
      </div>

      <div className="page-grid two-up">
        <Panel title="Scale and review candidates" subtitle="Experiments that need a decision or sponsor attention.">
          <div className="stack">
            {scaleCandidates.map((item) => (
              <Link key={item.id} to={`/experiments?team=${team}&experiment=${item.id}`} className="row-link-card">
                <div className="row-link-head">
                  <strong>{item.name}</strong>
                  <span className="stage-badge">{item.stage}</span>
                </div>
                <p>{item.summary}</p>
                <small>{item.targetMetric}: {item.pilotResult}</small>
              </Link>
            ))}
          </div>
        </Panel>

        <Panel title="Guided entry points" subtitle="Use the operating system by workflow, not by tool.">
          <div className="stack">
            {scenarios.map((scenario) => (
              <Link key={scenario.id} to={`/workspace?team=${team}&scenario=${scenario.id}`} className="row-link-card">
                <div className="row-link-head">
                  <strong>{scenario.title}</strong>
                  <ToneBadge tone="calm">{scenario.memberMoment}</ToneBadge>
                </div>
                <p>{scenario.summary}</p>
              </Link>
            ))}
          </div>
        </Panel>
      </div>

      {canViewAudit ? (
        <Panel title="Recent audit activity" subtitle="Proof that copilot runs and review actions are logged as operating events.">
          {auditState.loading && !auditEvents.length ? (
            <LoadingState title="Loading audit history" body="Fetching the most recent backend audit events." compact />
          ) : auditState.error && !auditEvents.length ? (
            <ErrorState title="Audit trail unavailable" body={auditState.error} compact />
          ) : auditEvents.length ? (
            <div className="stack">
              {auditEvents.slice(0, 5).map((event) => (
                <div key={event.id} className="row-link-card">
                  <div className="row-link-head">
                    <strong>{event.action.replace(/_/g, ' ')}</strong>
                    <ToneBadge tone="info">{event.entityType}</ToneBadge>
                  </div>
                  <p>{event.detail}</p>
                  <small>{event.id} · {new Date(event.createdAt).toLocaleString()}</small>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No audit events yet" body="Copilot runs and review actions will appear here once they are recorded." />
          )}
        </Panel>
      ) : null}
    </div>
  );
}
