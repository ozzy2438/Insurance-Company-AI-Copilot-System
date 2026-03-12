import { useAppState, useRouteTeam } from '../app-state';
import { api } from '../api/client';
import { EmptyState, ErrorState, LoadingState, PageHero, Panel, ToneBadge } from '../components';
import { useApiResource } from '../hooks/useApiResource';

export function AdoptionAcademyPage() {
  const team = useRouteTeam();
  const { selectedPersonaId } = useAppState();
  const academyState = useApiResource(() => api.getAcademy(team, selectedPersonaId), [team, selectedPersonaId]);
  const tracks = academyState.data?.trainingTracks ?? [];

  if (academyState.loading && !tracks.length) {
    return <LoadingState title="Loading adoption academy" body="Fetching enablement tracks, coaching packs, and champion coverage data." />;
  }

  if (academyState.error && !tracks.length) {
    return <ErrorState title="Adoption academy unavailable" body={academyState.error} />;
  }

  return (
    <div className="page-stack">
      <PageHero
        eyebrow="Enablement and change"
        title="Adoption academy"
        description="The operating layer for role-based training, manager coaching, champion coverage, and safe-use reinforcement."
      />

      <div className="page-grid two-up">
        <Panel title="Adoption principles" subtitle="How AI capability is embedded into team routines.">
          <ul className="simple-list">
            <li>Every new workflow ships with training, not only prompts.</li>
            <li>Managers are coached to recognise safe use, weak prompts, and escalation boundaries.</li>
            <li>Champion coverage is tracked because local adoption support drives reuse quality.</li>
          </ul>
        </Panel>

        <Panel title="Operating rhythm" subtitle="A practical change cadence rather than one-off workshops.">
          <div className="stack">
            <div className="row-stat"><span>Weekly</span><strong>Champion office hours</strong></div>
            <div className="row-stat"><span>Fortnightly</span><strong>Prompt quality clinics</strong></div>
            <div className="row-stat"><span>Monthly</span><strong>Experiment evidence review</strong></div>
          </div>
        </Panel>
      </div>

      <Panel title="Learning tracks" subtitle="Role-specific enablement designed to support real workflows.">
        {academyState.error && tracks.length ? <ErrorState title="Academy refresh issue" body={academyState.error} compact /> : null}
        {tracks.length ? (
          <div className="card-grid">
            {tracks.map((track) => (
              <article key={track.id} className="academy-card">
                <div className="row-link-head">
                  <strong>{track.title}</strong>
                  <ToneBadge tone={track.status === 'completed' ? 'positive' : track.status === 'at-risk' ? 'warning' : 'info'}>
                    {track.status}
                  </ToneBadge>
                </div>
                <p>{track.audience} · owner {track.owner}</p>
                <div className="progress-shell">
                  <div className="progress-fill" style={{ width: `${track.completion}%` }} />
                </div>
                <small>{track.completion}% complete · next session {track.nextSession}</small>
                <ul className="simple-list compact">
                  {track.modules.map((module) => (
                    <li key={module}>{module}</li>
                  ))}
                </ul>
              </article>
            ))}
          </div>
        ) : (
          <EmptyState title="No learning tracks" body="This team does not yet have any learning tracks in the backend sandbox." />
        )}
      </Panel>
    </div>
  );
}
