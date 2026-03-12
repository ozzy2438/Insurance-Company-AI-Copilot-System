import { Navigate, Route, Routes } from 'react-router-dom';
import { AppStateProvider } from './app-state';
import { AppShell } from './components';
import { AdoptionAcademyPage } from './pages/AdoptionAcademyPage';
import { CopilotWorkspacePage } from './pages/CopilotWorkspacePage';
import { ExperimentPortfolioPage } from './pages/ExperimentPortfolioPage';
import { GovernancePage } from './pages/GovernancePage';
import { ImpactPage } from './pages/ImpactPage';
import { KnowledgeHubPage } from './pages/KnowledgeHubPage';
import { OverviewPage } from './pages/OverviewPage';

export function App() {
  return (
    <AppStateProvider>
      <AppShell>
        <Routes>
          <Route element={<Navigate replace to="/overview?team=roadside" />} path="/" />
          <Route element={<OverviewPage />} path="/overview" />
          <Route element={<CopilotWorkspacePage />} path="/workspace" />
          <Route element={<ExperimentPortfolioPage />} path="/experiments" />
          <Route element={<GovernancePage />} path="/governance" />
          <Route element={<KnowledgeHubPage />} path="/knowledge" />
          <Route element={<AdoptionAcademyPage />} path="/academy" />
          <Route element={<ImpactPage />} path="/impact" />
        </Routes>
      </AppShell>
    </AppStateProvider>
  );
}
