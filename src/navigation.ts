export const appRoutes = [
  { path: '/overview', label: 'Overview', caption: 'Adoption health and operating pulse' },
  { path: '/workspace', label: 'Copilot Workspace', caption: 'Role-based copilots and guided drafting' },
  { path: '/experiments', label: 'Experiment Portfolio', caption: 'Pipeline, pilots, and scale decisions' },
  { path: '/governance', label: 'Governance & Risk', caption: 'Controls, approvals, and review points' },
  { path: '/knowledge', label: 'Knowledge Hub', caption: 'Prompts, playbooks, and reusable assets' },
  { path: '/academy', label: 'Adoption Academy', caption: 'Training, coaching, and champions' },
  { path: '/impact', label: 'Impact & KPIs', caption: 'Business outcomes and scale-readiness' },
] as const;
