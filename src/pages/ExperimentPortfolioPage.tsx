import { useDeferredValue, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { useAppState, useRouteTeam } from '../app-state';
import { api } from '../api/client';
import { DetailDrawer, EmptyState, ErrorState, LoadingState, PageHero, Panel, StageBadge, ToneBadge } from '../components';
import { useApiResource } from '../hooks/useApiResource';

export function ExperimentPortfolioPage() {
  const team = useRouteTeam();
  const { selectedPersonaId } = useAppState();
  const [searchParams, setSearchParams] = useSearchParams();
  const [stageFilter, setStageFilter] = useState<'all' | 'pipeline' | 'in-flight' | 'completed'>('all');
  const [search, setSearch] = useState('');
  const [actionMessage, setActionMessage] = useState<string | null>(null);
  const deferredSearch = useDeferredValue(search);
  const experimentsState = useApiResource(() => api.getExperiments(team, selectedPersonaId), [team, selectedPersonaId]);
  const governanceState = useApiResource(() => api.getGovernance(team, selectedPersonaId), [team, selectedPersonaId]);
  const knowledgeState = useApiResource(() => api.getKnowledge(team, selectedPersonaId), [team, selectedPersonaId]);
  const allExperiments = experimentsState.data ?? [];
  const experiments = allExperiments.filter((experiment) => {
    const matchesStage = stageFilter === 'all' || experiment.stage === stageFilter;
    const matchesSearch =
      !deferredSearch ||
      [experiment.name, experiment.owner, experiment.targetMetric].some((value) =>
        value.toLowerCase().includes(deferredSearch.toLowerCase())
      );
    return matchesStage && matchesSearch;
  });
  const selectedId = searchParams.get('experiment');
  const selected = allExperiments.find((item) => item.id === selectedId);
  const reviews = governanceState.data ?? [];
  const assets = knowledgeState.data ?? [];

  if (experimentsState.loading && !allExperiments.length) {
    return <LoadingState title="Loading experiment portfolio" body="Fetching the portfolio register, linked controls, and reusable assets." />;
  }

  if (experimentsState.error && !allExperiments.length) {
    return <ErrorState title="Experiment portfolio unavailable" body={experimentsState.error} />;
  }

  async function logExperimentAction(action: string, detail: string) {
    if (!selected) {
      return;
    }
    try {
      const result = await api.createExperimentAction(selected.id, action, detail, selectedPersonaId);
      setActionMessage(`Action recorded under audit event ${result.auditEventId}.`);
    } catch (error: unknown) {
      setActionMessage(error instanceof Error ? error.message : 'Unable to record experiment action.');
    }
  }

  return (
    <div className="page-stack">
      <PageHero
        eyebrow="Portfolio management"
        title="Experiment portfolio"
        description="Track the full AI experiment pipeline from intake to scale decision, with risk posture, evidence, and linked assets visible in one place."
      />

      <div className="filter-bar">
        <input
          className="search-input"
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search experiments, owners, or target metrics"
          value={search}
        />
        <div className="segmented-control">
          {(['all', 'pipeline', 'in-flight', 'completed'] as const).map((filter) => (
            <button
              key={filter}
              className={`segment${stageFilter === filter ? ' active' : ''}`}
              onClick={() => setStageFilter(filter)}
              type="button"
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      <div className="page-grid two-up">
        <Panel title="Portfolio pulse" subtitle="A compact view of scale-readiness across the team.">
          <div className="stack">
            <div className="row-stat">
              <span>Pipeline</span>
              <strong>{allExperiments.filter((item) => item.stage === 'pipeline').length}</strong>
            </div>
            <div className="row-stat">
              <span>In flight</span>
              <strong>{allExperiments.filter((item) => item.stage === 'in-flight').length}</strong>
            </div>
            <div className="row-stat">
              <span>Completed</span>
              <strong>{allExperiments.filter((item) => item.stage === 'completed').length}</strong>
            </div>
          </div>
        </Panel>

        <Panel title="Decision framing" subtitle="Scale decisions are tied to evidence and controls.">
          <ul className="simple-list">
            <li>Every pilot tracks baseline and pilot result against an agreed operational metric.</li>
            <li>Risk posture and open governance items are visible before scale decisions are made.</li>
            <li>Knowledge assets and training coverage are treated as scale dependencies.</li>
          </ul>
        </Panel>
      </div>

      {experimentsState.error && allExperiments.length ? (
        <ErrorState title="Portfolio refresh issue" body={experimentsState.error} compact />
      ) : null}

      <Panel title="Experiment register" subtitle="A product-style portfolio view rather than a static list.">
        {experiments.length ? (
          <div className="stack">
            {experiments.map((experiment) => (
              <button
                key={experiment.id}
                className="portfolio-row"
                onClick={() => {
                  const next = new URLSearchParams(searchParams);
                  next.set('team', team);
                  next.set('experiment', experiment.id);
                  setSearchParams(next);
                }}
                type="button"
              >
                <div className="portfolio-primary">
                  <div className="row-link-head">
                    <strong>{experiment.name}</strong>
                    <StageBadge value={experiment.stage} />
                  </div>
                  <p>{experiment.summary}</p>
                </div>
                <div className="portfolio-metrics">
                  <div>
                    <span>Owner</span>
                    <strong>{experiment.owner}</strong>
                  </div>
                  <div>
                    <span>Metric</span>
                    <strong>{experiment.targetMetric}</strong>
                  </div>
                  <div>
                    <span>Pilot result</span>
                    <strong>{experiment.pilotResult}</strong>
                  </div>
                  <ToneBadge
                    tone={
                      experiment.decision === 'scale'
                        ? 'positive'
                        : experiment.decision === 'iterate'
                          ? 'warning'
                          : experiment.decision === 'stop'
                            ? 'critical'
                            : 'info'
                    }
                  >
                    {experiment.decision}
                  </ToneBadge>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <EmptyState title="No experiments found" body="Adjust the stage filter or search term to see more portfolio records." />
        )}
      </Panel>

      {selected ? (
        <DetailDrawer
          title={selected.name}
          subtitle={`${selected.targetMetric} · ${selected.owner}`}
          onClose={() => {
            const next = new URLSearchParams(searchParams);
            next.delete('experiment');
            next.set('team', team);
            setSearchParams(next);
          }}
        >
          <div className="stack">
            {actionMessage ? <div className="info-block"><strong>Audit note</strong><p>{actionMessage}</p></div> : null}
            <div className="meta-grid">
              <div className="info-block">
                <strong>Baseline</strong>
                <p>{selected.baseline}</p>
              </div>
              <div className="info-block">
                <strong>Pilot result</strong>
                <p>{selected.pilotResult}</p>
              </div>
            </div>

            <div className="info-block">
              <strong>Dependencies</strong>
              <ul className="simple-list">
                {selected.dependencies.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="info-block">
              <strong>Timeline</strong>
              <div className="timeline">
                {selected.timeline.map((item) => (
                  <div key={`${item.date}-${item.label}`} className="timeline-item">
                    <small>{item.date}</small>
                    <strong>{item.label}</strong>
                    <p>{item.detail}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="info-block">
              <strong>Linked controls and assets</strong>
              <div className="stack">
                {selected.linkedGovernanceIds.map((id) => {
                  const review = reviews.find((item) => item.id === id);
                  return review ? (
                    <Link key={id} className="text-link" to={`/governance?team=${team}&review=${id}`}>
                      Governance: {review.title}
                    </Link>
                  ) : null;
                })}
                {selected.linkedKnowledgeIds.map((id) => {
                  const asset = assets.find((item) => item.id === id);
                  return asset ? (
                    <Link key={id} className="text-link" to={`/knowledge?team=${team}&asset=${id}`}>
                      Asset: {asset.title}
                    </Link>
                  ) : null;
                })}
              </div>
            </div>
            <div className="badge-row">
              <button
                className="primary-button"
                onClick={() =>
                  logExperimentAction(
                    'scale_review_logged',
                    `Scale review logged for ${selected.name}; current decision posture ${selected.decision}.`
                  )
                }
                type="button"
              >
                Record scale review
              </button>
              <button
                className="ghost-button"
                onClick={() =>
                  logExperimentAction(
                    'evidence_checkpoint',
                    `Evidence checkpoint recorded for ${selected.name}; pilot result ${selected.pilotResult}.`
                  )
                }
                type="button"
              >
                Record evidence checkpoint
              </button>
            </div>
          </div>
        </DetailDrawer>
      ) : null}
    </div>
  );
}
