export type TeamId = 'roadside' | 'claims' | 'contact-centre';

export type ExperimentStage = 'pipeline' | 'in-flight' | 'completed';
export type Decision = 'scale' | 'iterate' | 'stop' | 'pending';
export type RiskLevel = 'low' | 'medium' | 'high';
export type GovernanceStatus = 'approved' | 'review' | 'blocked' | 'renewal-due';
export type AssetStatus = 'approved' | 'draft' | 'retiring';
export type AssetType = 'prompt' | 'playbook' | 'policy' | 'copilot-studio' | 'workflow';
export type LearningStatus = 'on-track' | 'at-risk' | 'completed';
export type Severity = 'info' | 'warning' | 'critical';
export type MessageRole = 'user' | 'assistant';

export interface TeamContext {
  id: TeamId;
  label: string;
  shortLabel: string;
  strapline: string;
  operatingGoal: string;
  lead: string;
  liveExperiments: number;
  adoptionRate: number;
  governanceScore: number;
}

export interface KpiMetric {
  id: string;
  team: TeamId;
  label: string;
  value: string;
  change: string;
  direction: 'up' | 'down' | 'flat';
  target: string;
  note: string;
}

export interface AlertItem {
  id: string;
  team: TeamId;
  severity: Severity;
  title: string;
  body: string;
  route: string;
}

export interface ScenarioReference {
  title: string;
  type: 'policy' | 'guide' | 'playbook';
  detail: string;
}

export interface ChatMessage {
  role: MessageRole;
  content: string;
}

export interface CopilotScenario {
  id: string;
  team: TeamId;
  caseId: string;
  title: string;
  memberMoment: string;
  summary: string;
  objective: string;
  recommendedPrompt: string;
  humanReviewPoints: string[];
  references: ScenarioReference[];
  draftOutput: string[];
  cannedConversation: ChatMessage[];
  linkedAssetIds: string[];
}

export interface ExperimentTimelineEvent {
  date: string;
  label: string;
  detail: string;
}

export interface ExperimentRecord {
  id: string;
  team: TeamId;
  name: string;
  owner: string;
  stage: ExperimentStage;
  risk: RiskLevel;
  targetMetric: string;
  baseline: string;
  pilotResult: string;
  decision: Decision;
  summary: string;
  dependencies: string[];
  linkedGovernanceIds: string[];
  linkedKnowledgeIds: string[];
  timeline: ExperimentTimelineEvent[];
}

export interface GovernanceReview {
  id: string;
  team: TeamId;
  title: string;
  owner: string;
  risk: RiskLevel;
  status: GovernanceStatus;
  dueDate: string;
  controls: string[];
  exceptions: string[];
  linkedExperimentIds: string[];
}

export interface KnowledgeAsset {
  id: string;
  team: TeamId;
  type: AssetType;
  title: string;
  description: string;
  owner: string;
  status: AssetStatus;
  tags: string[];
  usageCount: number;
  rating: number;
  excerpt: string;
}

export interface TrainingTrack {
  id: string;
  team: TeamId;
  title: string;
  audience: string;
  owner: string;
  completion: number;
  status: LearningStatus;
  nextSession: string;
  modules: string[];
}

export interface ImpactStory {
  id: string;
  team: TeamId;
  title: string;
  baseline: string;
  current: string;
  evidence: string[];
}

export interface PermissionScope {
  teamId: TeamId;
  canReviewGovernance: boolean;
  canRunCopilot: boolean;
}

export interface Persona {
  id: string;
  name: string;
  title: string;
  description: string;
  defaultTeamId: TeamId;
  canViewAudit: boolean;
  permissionScopes: PermissionScope[];
}

export interface SessionData {
  activePersona: Persona;
  personas: Persona[];
  accessibleTeams: TeamContext[];
}

export interface MemberProfile {
  id: string;
  fullName: string;
  segment: string;
  membershipTier: string;
  postcode: string;
  vulnerabilityFlags: string[];
}

export interface ProductPolicy {
  id: string;
  team: TeamId;
  productName: string;
  status: string;
  renewalDate: string;
  coverageSummary: string;
}

export interface InteractionEvent {
  id: number;
  channel: string;
  occurredAt: string;
  summary: string;
}

export interface CaseRecord {
  id: string;
  memberId: string;
  team: TeamId;
  title: string;
  status: string;
  urgency: string;
  openedAt: string;
  summary: string;
  assignedTeam: string;
  owner: string;
}

export interface CaseContext {
  caseRecord: CaseRecord;
  member: MemberProfile;
  productPolicies: ProductPolicy[];
  interactions: InteractionEvent[];
}

export interface Citation {
  title: string;
  type: string;
  detail: string;
}

export interface RiskFlag {
  level: string;
  text: string;
}

export interface CopilotRunRequest {
  teamId: TeamId;
  scenarioId: string;
  caseId: string;
  mode: 'demo' | 'live';
  userInput: string;
}

export interface CopilotRunResult {
  runId: string;
  auditEventId: string;
  providerUsed: string;
  summary: string;
  recommendedAction: string;
  draft: string;
  citations: Citation[];
  riskFlags: RiskFlag[];
  humanReviewPoints: string[];
}

export interface ActionResponse {
  status: string;
  auditEventId: string;
}

export interface AuditEvent {
  id: string;
  personaId: string;
  teamId: TeamId;
  entityType: string;
  entityId: string;
  action: string;
  detail: string;
  createdAt: string;
}

export interface OverviewResponse {
  team: TeamContext;
  kpis: KpiMetric[];
  alerts: AlertItem[];
  scenarios: CopilotScenario[];
  scaleCandidates: ExperimentRecord[];
  trainingTracks: TrainingTrack[];
  knowledgeAssets: KnowledgeAsset[];
}

export interface AcademyResponse {
  team: TeamContext;
  trainingTracks: TrainingTrack[];
}

export interface ImpactResponse {
  team: TeamContext;
  kpis: KpiMetric[];
  stories: ImpactStory[];
}
