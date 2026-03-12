import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { useAppState, useRouteTeam } from '../app-state';
import { api } from '../api/client';
import { DetailDrawer, EmptyState, ErrorState, LoadingState, PageHero, Panel, ToneBadge } from '../components';
import { useApiResource } from '../hooks/useApiResource';
import type { ChatMessage, CopilotRunResult } from '../types';

function buildAssistantReply(result: CopilotRunResult) {
  return [
    `Operational summary: ${result.summary}`,
    `Recommended next action: ${result.recommendedAction}`,
    `Draft output: ${result.draft}`,
    `Human review points: ${result.humanReviewPoints.join(' | ')}`,
  ].join('\n\n');
}

export function CopilotWorkspacePage() {
  const team = useRouteTeam();
  const { selectedPersonaId } = useAppState();
  const [searchParams, setSearchParams] = useSearchParams();
  const scenariosState = useApiResource(() => api.getScenarios(team, selectedPersonaId), [team, selectedPersonaId]);
  const scenarios = scenariosState.data ?? [];
  const scenarioId = searchParams.get('scenario') ?? scenarios[0]?.id;
  const selectedScenario = scenarios.find((item) => item.id === scenarioId) ?? scenarios[0];
  const [mode, setMode] = useState<'demo' | 'live'>('demo');
  const [messages, setMessages] = useState<ChatMessage[]>(selectedScenario?.cannedConversation ?? []);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(Boolean(searchParams.get('scenario')));
  const [runResult, setRunResult] = useState<CopilotRunResult | null>(null);
  const [runError, setRunError] = useState<string | null>(null);

  const caseState = useApiResource(
    () => (selectedScenario ? api.getCaseContext(selectedScenario.caseId, selectedPersonaId) : Promise.resolve(null)),
    [selectedScenario?.caseId, selectedPersonaId]
  );

  useEffect(() => {
    setMessages(selectedScenario?.cannedConversation ?? []);
    setInput(selectedScenario?.recommendedPrompt ?? '');
    setRunResult(null);
    setRunError(null);
  }, [selectedScenario]);

  useEffect(() => {
    setDrawerOpen(Boolean(searchParams.get('scenario')));
  }, [searchParams]);

  if (scenariosState.loading && !scenarios.length) {
    return <LoadingState title="Loading copilot workspace" body="Resolving scenarios, cases, and governed references from the backend." />;
  }

  if (scenariosState.error && !scenarios.length) {
    return <ErrorState title="Workspace unavailable" body={scenariosState.error} />;
  }

  if (!selectedScenario) {
    return <EmptyState title="No scenarios available" body="The selected team does not yet have any backend-backed scenarios." />;
  }

  async function handleSend() {
    const trimmed = input.trim();
    if (!trimmed || loading) {
      return;
    }

    const nextMessages: ChatMessage[] = [...messages, { role: 'user', content: trimmed }];
    setMessages(nextMessages);
    setInput('');
    setLoading(true);
    setRunError(null);

    try {
      const result = await api.createCopilotRun(
        {
          teamId: team,
          scenarioId: selectedScenario.id,
          caseId: selectedScenario.caseId,
          mode,
          userInput: trimmed,
        },
        selectedPersonaId
      );
      setRunResult(result);
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: buildAssistantReply(result),
        },
      ]);
      if (mode === 'live' && result.providerUsed !== 'ollama-live') {
        setRunError('Live local generation was not available, so the backend returned a synthetic governed response instead.');
      }
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Unable to create a copilot run.';
      setRunError(message);
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: `Copilot run failed: ${message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-stack">
      <PageHero
        eyebrow="Operational copilots"
        title={`${selectedScenario.title}`}
        description="A guided workspace that keeps scenario context, approved references, human review points, and drafting support in one operational view."
        action={
          <div className="hero-actions">
            <button className={`mode-toggle${mode === 'demo' ? ' active' : ''}`} onClick={() => setMode('demo')} type="button">
              Demo mode
            </button>
            <button className={`mode-toggle${mode === 'live' ? ' active' : ''}`} onClick={() => setMode('live')} type="button">
              Live local mode
            </button>
          </div>
        }
      />

      <div className="workspace-layout">
        <Panel title="Scenario library" subtitle="Switch the workflow lens rather than opening a blank chat.">
          {scenariosState.error && scenarios.length ? (
            <ErrorState title="Scenario refresh issue" body={scenariosState.error} compact />
          ) : null}
          <div className="stack">
            {scenarios.map((scenario) => (
              <button
                key={scenario.id}
                className={`scenario-card${scenario.id === selectedScenario.id ? ' active' : ''}`}
                onClick={() => {
                  const next = new URLSearchParams(searchParams);
                  next.set('team', team);
                  next.set('scenario', scenario.id);
                  setSearchParams(next);
                }}
                type="button"
              >
                <div className="row-link-head">
                  <strong>{scenario.title}</strong>
                  <ToneBadge tone="info">{scenario.memberMoment}</ToneBadge>
                </div>
                <p>{scenario.summary}</p>
              </button>
            ))}
          </div>
        </Panel>

        <Panel
          title="AI workbench"
          subtitle="Backend-orchestrated drafting with synthetic context assembly, audit logging, and optional live local enhancement."
          action={
            <ToneBadge tone={mode === 'demo' ? 'calm' : runResult?.providerUsed === 'ollama-live' ? 'positive' : 'warning'}>
              {mode === 'demo' ? 'Synthetic mode' : runResult?.providerUsed === 'ollama-live' ? 'Ollama live' : 'Live fallback safe'}
            </ToneBadge>
          }
        >
          <div className="workspace-chat">
            <div className="message-list">
              {messages.map((message, index) => (
                <div key={`${message.role}-${index}`} className={`message-card ${message.role}`}>
                  <span>{message.role === 'assistant' ? 'Copilot' : 'User'}</span>
                  <p>{message.content}</p>
                </div>
              ))}
              {loading ? <div className="message-card assistant"><span>Copilot</span><p>Generating guided output...</p></div> : null}
            </div>

            <div className="composer">
              <textarea
                className="textarea"
                onChange={(event) => setInput(event.target.value)}
                placeholder="Ask for a summary, next-step recommendation, or a draft output."
                rows={4}
                value={input}
              />
              <div className="composer-footer">
                <small>Every run is assembled and logged by the backend. Live mode only upgrades the draft narrative if Ollama is available.</small>
                <button className="primary-button" onClick={handleSend} type="button">
                  Generate response
                </button>
              </div>
            </div>

            {runError ? <ErrorState title="Copilot run note" body={runError} compact /> : null}
          </div>
        </Panel>

        <Panel title="Guardrails and evidence" subtitle="Every output is anchored to approved references and review points.">
          <div className="stack">
            {caseState.loading && !caseState.data ? (
              <LoadingState title="Loading case context" body="Fetching member, policy, and interaction data for this scenario." compact />
            ) : null}
            {caseState.error ? <ErrorState title="Case context unavailable" body={caseState.error} compact /> : null}
            {caseState.data ? (
              <div className="info-block">
                <strong>Live case context</strong>
                <p>{caseState.data.caseRecord.summary}</p>
                <div className="badge-row">
                  <ToneBadge tone="info">{caseState.data.caseRecord.status}</ToneBadge>
                  <ToneBadge tone={caseState.data.caseRecord.urgency === 'High' ? 'critical' : 'warning'}>
                    {caseState.data.caseRecord.urgency} urgency
                  </ToneBadge>
                </div>
                <small>
                  Member: {caseState.data.member.fullName} · Tier {caseState.data.member.membershipTier} · Owner {caseState.data.caseRecord.owner}
                </small>
              </div>
            ) : null}
            <div className="info-block">
              <strong>Recommended prompt starter</strong>
              <p>{selectedScenario.recommendedPrompt}</p>
            </div>
            <div className="info-block">
              <strong>Human review points</strong>
              <ul className="simple-list">
                {(runResult?.humanReviewPoints ?? selectedScenario.humanReviewPoints).map((point) => (
                  <li key={point}>{point}</li>
                ))}
              </ul>
            </div>
            <div className="info-block">
              <strong>Reference set</strong>
              <div className="stack">
                {(runResult?.citations ?? selectedScenario.references).map((reference) => (
                  <div key={reference.title} className="reference-card">
                    <div className="row-link-head">
                      <strong>{reference.title}</strong>
                      <ToneBadge tone="calm">{reference.type}</ToneBadge>
                    </div>
                    <p>{reference.detail}</p>
                  </div>
                ))}
              </div>
            </div>
            {runResult ? (
              <>
                <div className="info-block">
                  <strong>Run metadata</strong>
                  <p>Provider: {runResult.providerUsed} · Audit event: {runResult.auditEventId}</p>
                </div>
                <div className="info-block">
                  <strong>Risk flags</strong>
                  <ul className="simple-list">
                    {runResult.riskFlags.map((flag) => (
                      <li key={`${flag.level}-${flag.text}`}>{flag.level}: {flag.text}</li>
                    ))}
                  </ul>
                </div>
              </>
            ) : null}
            <Link className="text-link" to={`/knowledge?team=${team}`}>
              Open related assets in Knowledge Hub
            </Link>
          </div>
        </Panel>
      </div>

      {drawerOpen ? (
        <DetailDrawer
          title={selectedScenario.title}
          subtitle={selectedScenario.objective}
          onClose={() => {
            const next = new URLSearchParams(searchParams);
            next.delete('scenario');
            next.set('team', team);
            setSearchParams(next);
          }}
        >
          <div className="stack">
            <div className="info-block">
              <strong>Draft output example</strong>
              <ul className="simple-list">
                {selectedScenario.draftOutput.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            {caseState.data ? (
              <div className="info-block">
                <strong>Interaction history</strong>
                <ul className="simple-list compact">
                  {caseState.data.interactions.map((item) => (
                    <li key={item.id}>{item.occurredAt} · {item.channel}: {item.summary}</li>
                  ))}
                </ul>
              </div>
            ) : null}
            <div className="info-block">
              <strong>Usage note</strong>
              <p>This workspace intentionally shows AI as one capability inside a governed operating model. The agent supports decisions; it does not own them.</p>
            </div>
          </div>
        </DetailDrawer>
      ) : null}
    </div>
  );
}
