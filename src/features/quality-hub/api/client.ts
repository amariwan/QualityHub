import {
  PipelinesResponse,
  PortfolioResponse,
  ProjectMatrixResponse,
  Team,
  TeamMember
} from '@/features/quality-hub/types';

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/v1';

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {})
    },
    ...init
  });

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = (await response.json()) as { detail?: string };
      detail = body.detail || detail;
    } catch {
      // ignore
    }
    throw new Error(detail);
  }

  return response.json() as Promise<T>;
}

export function connectGitlabToken(payload: {
  token: string;
  base_url?: string;
}) {
  return apiFetch<{
    user_id: number;
    email: string;
    gitlab_connected: boolean;
  }>('/auth/token', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export function getAuthMe() {
  return apiFetch<{
    user_id: number;
    email: string;
    gitlab_connected: boolean;
  }>('/auth/me');
}

export function disconnectGitlabToken() {
  return apiFetch<{ status: string }>('/auth/token', {
    method: 'DELETE'
  });
}

export function getPortfolio(params: {
  showClusters: boolean;
  scope?: string;
}) {
  const query = new URLSearchParams({
    show_clusters: String(params.showClusters)
  });
  return apiFetch<PortfolioResponse>(`/deployments/status?${query.toString()}`);
}

export function getProjectMatrix(projectId: number) {
  return apiFetch<ProjectMatrixResponse>(`/deployments/status/${projectId}`);
}

export function getPipelines(scope: 'all' | 'readiness') {
  return apiFetch<PipelinesResponse>(`/pipelines?scope=${scope}`);
}

export function triggerProjectSync() {
  return apiFetch<{ sync_run_id: number; celery_job_id: string }>(
    '/projects/sync',
    {
      method: 'POST',
      body: JSON.stringify({ trigger: 'manual' })
    }
  );
}

export function listTeams() {
  return apiFetch<Team[]>('/teams');
}

export function createTeam(payload: { name: string }) {
  return apiFetch<Team>('/teams', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export function listTeamMembers(teamId: number) {
  return apiFetch<TeamMember[]>(`/teams/${teamId}/members`);
}

export function addTeamMember(
  teamId: number,
  payload: { user_id: number; role: string }
) {
  return apiFetch<TeamMember>(`/teams/${teamId}/members`, {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export function listWorkspaceViews() {
  return apiFetch<
    Array<{
      id: number;
      name: string;
      visibility: string;
      team_id: number | null;
      definition_json: Record<string, unknown>;
    }>
  >('/workspace/views');
}

export function createWorkspaceView(payload: {
  name: string;
  visibility?: string;
  team_id?: number | null;
  definition_json?: Record<string, unknown>;
}) {
  return apiFetch('/workspace/views', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export function listWorkspaceNotes() {
  return apiFetch<
    Array<{
      id: number;
      visibility: string;
      scope_type: string;
      project_id: number | null;
      env: string | null;
      cluster_id: number | null;
      content: string;
    }>
  >('/workspace/notes');
}

export function createWorkspaceNote(payload: {
  content: string;
  visibility?: string;
  scope_type?: string;
  project_id?: number | null;
  env?: string | null;
  cluster_id?: number | null;
}) {
  return apiFetch('/workspace/notes', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export function listWorkspaceWatchlist() {
  return apiFetch<
    Array<{
      id: number;
      visibility: string;
      project_id: number;
      team_id: number | null;
    }>
  >('/workspace/watchlist');
}

export function createWorkspaceWatchlist(payload: {
  project_id: number;
  visibility?: string;
  team_id?: number | null;
}) {
  return apiFetch('/workspace/watchlist', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export function listWorkspaceTags() {
  return apiFetch<
    Array<{
      id: number;
      visibility: string;
      team_id: number | null;
      name: string;
      color: string | null;
      links: Array<{
        id: number;
        scope_type: string;
        project_id: number | null;
        env: string | null;
        cluster_id: number | null;
      }>;
    }>
  >('/workspace/tags');
}

export function createWorkspaceTag(payload: {
  name: string;
  color?: string | null;
  visibility?: string;
  team_id?: number | null;
  links?: Array<{
    scope_type: string;
    project_id?: number | null;
    env?: string | null;
    cluster_id?: number | null;
  }>;
}) {
  return apiFetch('/workspace/tags', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}
