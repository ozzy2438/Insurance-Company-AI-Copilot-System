import { type ReactNode } from 'react';
import { Link, NavLink, useLocation, useNavigate } from 'react-router-dom';
import { useAppState } from './app-state';
import { api } from './api/client';
import { useApiResource } from './hooks/useApiResource';
import { appRoutes } from './navigation';
import type { AlertItem } from './types';

export function AppShell({ children }: { children: ReactNode }) {
  const {
    accessibleTeams,
    currentTeam,
    error,
    loading,
    selectedPersonaId,
    selectedTeam,
    session,
    setSelectedPersonaId,
    setSelectedTeam,
  } = useAppState();
  const location = useLocation();
  const navigate = useNavigate();
  const selectedPersona = session?.personas.find((persona) => persona.id === selectedPersonaId) ?? session?.activePersona ?? null;

  const kpiState = useApiResource(
    () => (currentTeam ? api.getKpis(currentTeam.id, selectedPersonaId) : Promise.resolve([])),
    [currentTeam?.id, selectedPersonaId]
  );
  const alertState = useApiResource(
    () => (currentTeam ? api.getAlerts(currentTeam.id, selectedPersonaId) : Promise.resolve([])),
    [currentTeam?.id, selectedPersonaId]
  );

  const headlineMetrics = (kpiState.data ?? []).slice(0, 2);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-kicker">AI Adoption OS</div>
          <h1>Member Operations Copilot Command Centre</h1>
          <p>Operational copilots, governed knowledge, experiment scale, and measurable impact.</p>
        </div>

        <nav className="nav-stack">
          {appRoutes.map((route) => (
            <NavLink
              key={route.path}
              className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
              to={`${route.path}?team=${selectedTeam}`}
            >
              <span>{route.label}</span>
              <small>{route.caption}</small>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-card">
          <span className="eyebrow">Demo persona</span>
          {selectedPersona ? (
            <>
              <strong>{selectedPersona.title}</strong>
              <p>{selectedPersona.description}</p>
            </>
          ) : (
            <p>Loading persona session...</p>
          )}
        </div>
      </aside>

      <div className="workspace">
        <header className="topbar">
          <div>
            <div className="eyebrow">Transformation operating system</div>
            <h2>{currentTeam?.label ?? 'Loading team context'}</h2>
            <p>{currentTeam?.strapline ?? 'Resolving persona access and backend-backed team context.'}</p>
          </div>

          <div className="topbar-actions">
            <div className="persona-picker">
              <label htmlFor="persona-select">Demo persona</label>
              <select
                id="persona-select"
                value={selectedPersonaId}
                onChange={(event) => {
                  const nextPersonaId = event.target.value;
                  const persona = session?.personas.find((item) => item.id === nextPersonaId);
                  setSelectedPersonaId(nextPersonaId);
                  if (persona) {
                    setSelectedTeam(persona.defaultTeamId);
                    navigate(`${location.pathname}?team=${persona.defaultTeamId}`);
                  }
                }}
              >
                {(session?.personas ?? []).map((persona) => (
                  <option key={persona.id} value={persona.id}>
                    {persona.title}
                  </option>
                ))}
              </select>
            </div>

            <div className="team-switcher">
              {accessibleTeams.map((team) => (
                <button
                  key={team.id}
                  className={`team-switch${team.id === selectedTeam ? ' active' : ''}`}
                  onClick={() => {
                    setSelectedTeam(team.id);
                    navigate(`${location.pathname}?team=${team.id}`);
                  }}
                  type="button"
                >
                  {team.shortLabel}
                </button>
              ))}
            </div>

            <div className="topbar-metrics">
              {headlineMetrics.map((metric) => (
                <div key={metric.id} className="mini-metric">
                  <span>{metric.label}</span>
                  <strong>{metric.value}</strong>
                  <small>{metric.change}</small>
                </div>
              ))}
            </div>
          </div>
        </header>

        {loading && !session ? <LoadingState title="Loading backend session" body="Resolving demo persona, permissions, and accessible teams." /> : null}
        {error ? <ErrorState title="Session failed to load" body={error} /> : null}

        <div className="workspace-grid">
          <main className="main-column">{children}</main>
          <AlertRail alerts={alertState.data ?? []} error={alertState.error} loading={alertState.loading} />
        </div>
      </div>
    </div>
  );
}

export function AlertRail({
  alerts,
  loading,
  error,
}: {
  alerts: AlertItem[];
  loading: boolean;
  error: string | null;
}) {
  return (
    <aside className="alert-rail">
      <Panel
        title="Attention queue"
        subtitle="Backend-served signals that need action or review."
        action={<span className="meta-tag">{alerts.length} active</span>}
      >
        {loading ? <LoadingState title="Loading alerts" body="Fetching attention queue from the synthetic backend." compact /> : null}
        {error ? <ErrorState title="Alerts unavailable" body={error} compact /> : null}
        <div className="stack">
          {alerts.map((alert) => (
            <Link key={alert.id} className={`alert-card ${alert.severity}`} to={alert.route}>
              <div className="alert-topline">
                <ToneBadge tone={alert.severity}>{alert.severity}</ToneBadge>
                <span className="alert-route">{alert.title}</span>
              </div>
              <p>{alert.body}</p>
            </Link>
          ))}
        </div>
      </Panel>

      <Panel title="Operating principles" subtitle="Guardrails visible across every workflow.">
        <ul className="simple-list">
          <li>Human review remains explicit in member-impacting decisions.</li>
          <li>Only approved prompts and assets are pushed into reuse.</li>
          <li>Experiment scale is gated by evidence, not enthusiasm.</li>
        </ul>
      </Panel>
    </aside>
  );
}

export function Panel({
  title,
  subtitle,
  action,
  children,
}: {
  title: string;
  subtitle?: string;
  action?: ReactNode;
  children: ReactNode;
}) {
  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <h3>{title}</h3>
          {subtitle ? <p>{subtitle}</p> : null}
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}

export function MetricCard({
  label,
  value,
  change,
  note,
}: {
  label: string;
  value: string;
  change: string;
  note: string;
}) {
  const tone = change.includes('-') ? 'calm' : 'positive';

  return (
    <article className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <div className="metric-row">
        <ToneBadge tone={tone}>{change}</ToneBadge>
        <small>{note}</small>
      </div>
    </article>
  );
}

export function ToneBadge({
  tone,
  children,
}: {
  tone: 'positive' | 'warning' | 'critical' | 'calm' | 'info';
  children: ReactNode;
}) {
  return <span className={`tone-badge ${tone}`}>{children}</span>;
}

export function StageBadge({ value }: { value: string }) {
  return <span className={`stage-badge ${value.toLowerCase().replace(/\s+/g, '-')}`}>{value}</span>;
}

export function DetailDrawer({
  title,
  subtitle,
  children,
  onClose,
}: {
  title: string;
  subtitle?: string;
  children: ReactNode;
  onClose: () => void;
}) {
  return (
    <div className="drawer-backdrop" onClick={onClose} role="presentation">
      <aside className="detail-drawer" onClick={(event) => event.stopPropagation()}>
        <div className="drawer-header">
          <div>
            <div className="eyebrow">Detail view</div>
            <h3>{title}</h3>
            {subtitle ? <p>{subtitle}</p> : null}
          </div>
          <button className="ghost-button" onClick={onClose} type="button">
            Close
          </button>
        </div>
        <div className="drawer-body">{children}</div>
      </aside>
    </div>
  );
}

export function PageHero({
  eyebrow,
  title,
  description,
  action,
}: {
  eyebrow: string;
  title: string;
  description: string;
  action?: ReactNode;
}) {
  return (
    <section className="page-hero">
      <div>
        <div className="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      {action}
    </section>
  );
}

export function EmptyState({ title, body }: { title: string; body: string }) {
  return (
    <div className="empty-state">
      <strong>{title}</strong>
      <p>{body}</p>
    </div>
  );
}

export function LoadingState({
  title,
  body,
  compact = false,
}: {
  title: string;
  body: string;
  compact?: boolean;
}) {
  return (
    <div className={`empty-state${compact ? ' compact-state' : ''}`}>
      <strong>{title}</strong>
      <p>{body}</p>
    </div>
  );
}

export function ErrorState({
  title,
  body,
  compact = false,
}: {
  title: string;
  body: string;
  compact?: boolean;
}) {
  return (
    <div className={`empty-state error-state${compact ? ' compact-state' : ''}`}>
      <strong>{title}</strong>
      <p>{body}</p>
    </div>
  );
}
