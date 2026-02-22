export type DeploymentCluster = {
  cluster_id: number;
  cluster: string | null;
  status: 'ready' | 'progressing' | 'degraded' | 'failed' | 'unknown';
  updated_at: string | null;
};

export type DeploymentEnvironment = {
  env: string;
  status: 'ready' | 'progressing' | 'degraded' | 'failed' | 'unknown';
  clusters: DeploymentCluster[];
};

export type PortfolioItem = {
  project_id: number;
  project: string | null;
  environments: DeploymentEnvironment[];
};

export type PortfolioResponse = {
  user_id: number;
  show_clusters: boolean;
  items: PortfolioItem[];
};

export type PipelineItem = {
  id: number;
  project_id: number;
  gitlab_pipeline_id: number;
  status: string;
  ref: string | null;
  sha: string | null;
  source_type: string | null;
  deployability_state: 'deployable' | 'not_deployable' | 'partial_unknown';
  failure_reasons: string[];
  missing_signals: string[];
};

export type PipelinesResponse = {
  scope: 'all' | 'readiness';
  count: number;
  items: PipelineItem[];
};

export type ProjectMatrixResponse = {
  project_id: number;
  user_id: number;
  matrix: Record<string, Array<Record<string, string | number | null>>>;
};

export type Team = {
  id: number;
  name: string;
};

export type TeamMember = {
  id: number;
  team_id: number;
  user_id: number;
  role: string;
};
