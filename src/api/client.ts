import type {
  AcademyResponse,
  ActionResponse,
  AlertItem,
  AuditEvent,
  CaseContext,
  CopilotRunRequest,
  CopilotRunResult,
  ExperimentRecord,
  GovernanceReview,
  ImpactResponse,
  KpiMetric,
  KnowledgeAsset,
  OverviewResponse,
  SessionData,
  TeamId,
  CopilotScenario,
} from '../types';

const API_BASE = '/api';

async function request<T>(path: string, personaId?: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  if (personaId) {
    headers.set('X-Demo-Persona', personaId);
  }
  if (init?.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(`${API_BASE}${path}`, { ...init, headers });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  getSession: (personaId?: string) => request<SessionData>('/session', personaId),
  getOverview: (teamId: TeamId, personaId: string) => request<OverviewResponse>(`/teams/${teamId}/overview`, personaId),
  getKpis: (teamId: TeamId, personaId: string) => request<KpiMetric[]>(`/teams/${teamId}/kpis`, personaId),
  getAlerts: (teamId: TeamId, personaId: string) => request<AlertItem[]>(`/teams/${teamId}/alerts`, personaId),
  getScenarios: (teamId: TeamId, personaId: string) => request<CopilotScenario[]>(`/teams/${teamId}/scenarios`, personaId),
  getCaseContext: (caseId: string, personaId: string) => request<CaseContext>(`/cases/${caseId}/context`, personaId),
  getExperiments: (teamId: TeamId, personaId: string) => request<ExperimentRecord[]>(`/teams/${teamId}/experiments`, personaId),
  getGovernance: (teamId: TeamId, personaId: string) => request<GovernanceReview[]>(`/teams/${teamId}/governance`, personaId),
  getKnowledge: (teamId: TeamId, personaId: string) => request<KnowledgeAsset[]>(`/teams/${teamId}/knowledge`, personaId),
  getAcademy: (teamId: TeamId, personaId: string) => request<AcademyResponse>(`/teams/${teamId}/academy`, personaId),
  getImpact: (teamId: TeamId, personaId: string) => request<ImpactResponse>(`/teams/${teamId}/impact`, personaId),
  createCopilotRun: (payload: CopilotRunRequest, personaId: string) =>
    request<CopilotRunResult>('/copilot/runs', personaId, { method: 'POST', body: JSON.stringify(payload) }),
  createExperimentAction: (experimentId: string, action: string, detail: string, personaId: string) =>
    request<ActionResponse>(`/experiments/${experimentId}/actions`, personaId, {
      method: 'POST',
      body: JSON.stringify({ action, detail }),
    }),
  createGovernanceAction: (reviewId: string, action: string, detail: string, personaId: string) =>
    request<ActionResponse>(`/governance/${reviewId}/actions`, personaId, {
      method: 'POST',
      body: JSON.stringify({ action, detail }),
    }),
  getAuditEvents: (personaId: string, teamId?: TeamId) =>
    request<AuditEvent[]>(`/audit-events${teamId ? `?teamId=${teamId}` : ''}`, personaId),
};
