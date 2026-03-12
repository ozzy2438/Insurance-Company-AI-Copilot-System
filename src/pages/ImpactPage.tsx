import { useAppState, useRouteTeam } from '../app-state';
import { api } from '../api/client';
import { EmptyState, ErrorState, LoadingState, MetricCard, PageHero, Panel } from '../components';
import { useApiResource } from '../hooks/useApiResource';

export function ImpactPage() {
  const team = useRouteTeam();
  const { selectedPersonaId } = useAppState();
  const impactState = useApiResource(() => api.getImpact(team, selectedPersonaId), [team, selectedPersonaId]);
  const metrics = impactState.data?.kpis ?? [];
  const stories = impactState.data?.stories ?? [];

  if (impactState.loading && !metrics.length && !stories.length) {
    return <LoadingState title="Loading impact evidence" body="Fetching KPI trends and backed impact stories from the backend." />;
  }

  if (impactState.error && !metrics.length && !stories.length) {
    return <ErrorState title="Impact view unavailable" body={impactState.error} />;
  }

  return (
    <div className="page-stack">
      <PageHero
        eyebrow="Evidence and outcomes"
        title="Impact and KPIs"
        description="Operational outcomes tied to adoption, service quality, and experiment scale-readiness."
      />

      <div className="metric-grid">
        {metrics.map((metric) => (
          <MetricCard
            key={metric.id}
            label={metric.label}
            value={metric.value}
            change={metric.change}
            note={`Target ${metric.target}`}
          />
        ))}
      </div>

      {impactState.error && (metrics.length || stories.length) ? <ErrorState title="Impact refresh issue" body={impactState.error} compact /> : null}

      <Panel title="Impact stories" subtitle="Narratives backed by operational evidence, not only feature demos.">
        {stories.length ? (
          <div className="card-grid">
            {stories.map((story) => (
              <article key={story.id} className="knowledge-card">
                <strong>{story.title}</strong>
                <p>{story.baseline}</p>
                <p>{story.current}</p>
                <ul className="simple-list compact">
                  {story.evidence.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </article>
            ))}
          </div>
        ) : (
          <EmptyState title="No impact stories" body="The selected team does not yet have any impact evidence stories in the backend sandbox." />
        )}
      </Panel>
    </div>
  );
}
