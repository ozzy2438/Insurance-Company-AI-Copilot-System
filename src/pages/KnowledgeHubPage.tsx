import { useDeferredValue, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useAppState, useRouteTeam } from '../app-state';
import { api } from '../api/client';
import { DetailDrawer, EmptyState, ErrorState, LoadingState, PageHero, Panel, ToneBadge } from '../components';
import { useApiResource } from '../hooks/useApiResource';

export function KnowledgeHubPage() {
  const team = useRouteTeam();
  const { selectedPersonaId } = useAppState();
  const [searchParams, setSearchParams] = useSearchParams();
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState<'all' | 'prompt' | 'playbook' | 'policy' | 'copilot-studio' | 'workflow'>('all');
  const deferredSearch = useDeferredValue(search);
  const knowledgeState = useApiResource(() => api.getKnowledge(team, selectedPersonaId), [team, selectedPersonaId]);
  const allAssets = knowledgeState.data ?? [];
  const assets = allAssets.filter((asset) => {
    const matchesType = typeFilter === 'all' || asset.type === typeFilter;
    const matchesSearch =
      !deferredSearch ||
      [asset.title, asset.description, ...asset.tags].some((value) =>
        value.toLowerCase().includes(deferredSearch.toLowerCase())
    );
    return matchesType && matchesSearch;
  });
  const selected = allAssets.find((asset) => asset.id === searchParams.get('asset'));

  if (knowledgeState.loading && !allAssets.length) {
    return <LoadingState title="Loading knowledge hub" body="Fetching approved prompts, playbooks, and workflow assets from the backend." />;
  }

  if (knowledgeState.error && !allAssets.length) {
    return <ErrorState title="Knowledge hub unavailable" body={knowledgeState.error} />;
  }

  return (
    <div className="page-stack">
      <PageHero
        eyebrow="Governed reuse"
        title="Knowledge hub"
        description="Approved prompts, playbooks, workflow guides, and Copilot assets curated for operational reuse rather than ad hoc prompting."
      />

      <div className="filter-bar">
        <input
          className="search-input"
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search prompts, playbooks, tags, or asset descriptions"
          value={search}
        />
        <div className="segmented-control wrap">
          {(['all', 'prompt', 'playbook', 'policy', 'workflow', 'copilot-studio'] as const).map((filter) => (
            <button
              key={filter}
              className={`segment${typeFilter === filter ? ' active' : ''}`}
              onClick={() => setTypeFilter(filter)}
              type="button"
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      <Panel title="Approved assets" subtitle="Reusable assets that make adoption repeatable across teams.">
        {knowledgeState.error && allAssets.length ? <ErrorState title="Knowledge refresh issue" body={knowledgeState.error} compact /> : null}
        {assets.length ? (
          <div className="card-grid">
            {assets.map((asset) => (
              <button
                key={asset.id}
                className="knowledge-card"
                onClick={() => {
                  const next = new URLSearchParams(searchParams);
                  next.set('team', team);
                  next.set('asset', asset.id);
                  setSearchParams(next);
                }}
                type="button"
              >
                <div className="row-link-head">
                  <strong>{asset.title}</strong>
                  <ToneBadge tone={asset.status === 'approved' ? 'positive' : asset.status === 'draft' ? 'warning' : 'critical'}>
                    {asset.status}
                  </ToneBadge>
                </div>
                <p>{asset.description}</p>
                <div className="badge-row">
                  <ToneBadge tone="calm">{asset.type}</ToneBadge>
                  <span>{asset.usageCount} uses</span>
                  <span>{asset.rating.toFixed(1)} rating</span>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <EmptyState title="No assets match this filter" body="Broaden the search or switch asset type to see more reusable knowledge." />
        )}
      </Panel>

      {selected ? (
        <DetailDrawer
          title={selected.title}
          subtitle={`${selected.type} · owned by ${selected.owner}`}
          onClose={() => {
            const next = new URLSearchParams(searchParams);
            next.delete('asset');
            next.set('team', team);
            setSearchParams(next);
          }}
        >
          <div className="stack">
            <div className="info-block">
              <strong>Description</strong>
              <p>{selected.description}</p>
            </div>
            <div className="info-block">
              <strong>Excerpt</strong>
              <p>{selected.excerpt}</p>
            </div>
            <div className="info-block">
              <strong>Tags</strong>
              <div className="badge-row">
                {selected.tags.map((tag) => (
                  <ToneBadge key={tag} tone="info">
                    {tag}
                  </ToneBadge>
                ))}
              </div>
            </div>
          </div>
        </DetailDrawer>
      ) : null}
    </div>
  );
}
