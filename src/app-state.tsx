import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from './api/client';
import type { SessionData, TeamContext, TeamId } from './types';

interface AppStateValue {
  session: SessionData | null;
  selectedPersonaId: string;
  setSelectedPersonaId: (personaId: string) => void;
  selectedTeam: TeamId;
  setSelectedTeam: (team: TeamId) => void;
  accessibleTeams: TeamContext[];
  currentTeam: TeamContext | null;
  loading: boolean;
  error: string | null;
}

const AppStateContext = createContext<AppStateValue | null>(null);

function isTeamId(value: string | null): value is TeamId {
  return value === 'roadside' || value === 'claims' || value === 'contact-centre';
}

export function AppStateProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<SessionData | null>(null);
  const [selectedPersonaId, setSelectedPersonaId] = useState('transformation-lead');
  const [selectedTeam, setSelectedTeam] = useState<TeamId>('roadside');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    api
      .getSession(selectedPersonaId)
      .then((result) => {
        if (cancelled) {
          return;
        }
        setSession(result);
        const allowedTeamIds = result.accessibleTeams.map((team) => team.id);
        if (!allowedTeamIds.includes(selectedTeam)) {
          setSelectedTeam(result.activePersona.defaultTeamId ?? result.accessibleTeams[0]?.id ?? 'roadside');
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Unable to load session');
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [selectedPersonaId]);

  const accessibleTeams = session?.accessibleTeams ?? [];
  const currentTeam = accessibleTeams.find((team) => team.id === selectedTeam) ?? accessibleTeams[0] ?? null;

  return (
    <AppStateContext.Provider
      value={{
        session,
        selectedPersonaId,
        setSelectedPersonaId,
        selectedTeam,
        setSelectedTeam,
        accessibleTeams,
        currentTeam,
        loading,
        error,
      }}
    >
      {children}
    </AppStateContext.Provider>
  );
}

export function useAppState() {
  const value = useContext(AppStateContext);
  if (!value) {
    throw new Error('useAppState must be used inside AppStateProvider');
  }
  return value;
}

export function useRouteTeam() {
  const [searchParams] = useSearchParams();
  const { selectedTeam, setSelectedTeam, accessibleTeams } = useAppState();
  const routeTeam = searchParams.get('team');

  useEffect(() => {
    if (isTeamId(routeTeam) && accessibleTeams.some((team) => team.id === routeTeam) && routeTeam !== selectedTeam) {
      setSelectedTeam(routeTeam);
    }
  }, [accessibleTeams, routeTeam, selectedTeam, setSelectedTeam]);

  return isTeamId(routeTeam) && accessibleTeams.some((team) => team.id === routeTeam) ? routeTeam : selectedTeam;
}
