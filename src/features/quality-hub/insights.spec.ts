import { describe, expect, it } from 'vitest';
import type {
  DoraMetrics,
  OpsOverviewResponse,
  RiskRadarResponse
} from '@/features/quality-hub/types';
import {
  buildDoraForecast,
  buildIncidentDeploymentLinks,
  buildReleaseRiskScoreboard,
  buildRetroActionTracker,
  detectDoraAnomalies,
  simulateQualityGate
} from '@/features/quality-hub/insights';

const doraFixture: DoraMetrics = {
  window_days: 30,
  sample_size: 80,
  deployment_frequency: {
    deployments: 20,
    per_day: 0.67,
    per_week: 4.7,
    classification: 'high'
  },
  lead_time_hours: {
    value: 36,
    classification: 'medium'
  },
  change_failure_rate: {
    pct: 18,
    classification: 'low'
  },
  mttr_hours: {
    value: 12,
    classification: 'high'
  },
  overall_classification: 'medium',
  calculation_note: 'test fixture'
};

const riskRadarFixture = {
  release_risk: {
    distribution: { low: 0, medium: 1, high: 1 },
    projects: [
      {
        project_id: 10,
        project: 'alpha',
        score: 72,
        level: 'high',
        label: 'High'
      },
      {
        project_id: 11,
        project: 'beta',
        score: 38,
        level: 'medium',
        label: 'Medium'
      }
    ]
  },
  quality_trend: [
    { week: 'W1', score: 65, label: 'watch' },
    { week: 'W2', score: 72, label: 'stable' },
    { week: 'W3', score: 76, label: 'stable' },
    { week: 'W4', score: 81, label: 'stable' }
  ],
  regressions: [
    {
      project_id: 10,
      project: 'alpha',
      type: 'test_failures',
      severity: 'high',
      reason: 'Flaky test in smoke suite',
      current: 7,
      previous: 3
    }
  ],
  delivery_confidence: [
    {
      project_id: 10,
      project: 'alpha',
      value_pct: 62,
      mttr_hours: 10,
      flakiness_score_pct: 42
    },
    {
      project_id: 11,
      project: 'beta',
      value_pct: 90,
      mttr_hours: 2,
      flakiness_score_pct: 5
    }
  ],
  release_readiness: [
    { project_id: 10, project: 'alpha', value_pct: 68 },
    { project_id: 11, project: 'beta', value_pct: 88 }
  ],
  team_quality_indicator: [
    {
      team: 'Platform',
      stability: 'red',
      label: 'under pressure',
      project_count: 3
    }
  ],
  release_notes: {
    feed: [
      {
        version: 'v1.2.3',
        target_branch: 'main',
        date: '2026-02-01',
        project: 'alpha',
        category: 'bugfix',
        category_label: 'Bugfix',
        status: 'released',
        risk: { level: 'high', label: 'High', reason: 'hotfix' },
        why_relevant: 'test',
        known_issues: []
      }
    ],
    comparison: {
      new_features: 1,
      bugfixes: 1,
      security_fixes: 0,
      known_risks: 1
    }
  }
} as unknown as RiskRadarResponse;

const opsOverviewFixture = {
  incident_links: [
    {
      id: 901,
      workspace_id: 1,
      project_id: 10,
      project: 'alpha',
      pipeline_id: 44,
      gitlab_pipeline_id: 4044,
      provider: 'gitlab',
      external_issue_id: 'INC-901',
      external_url: null,
      title: 'alpha failure',
      status: 'open',
      created_at: '2026-02-20T10:00:00Z',
      updated_at: '2026-02-20T10:00:00Z'
    }
  ],
  ownership_heatmap: {
    summary: {
      projects_total: 2,
      teams_total: 1,
      unowned_projects: 1,
      overloaded_teams: 1
    },
    teams: [
      {
        team_id: 1,
        team: 'Platform',
        project_count: 3,
        status: 'overloaded',
        capacity_threshold: 2
      }
    ],
    projects: [],
    unowned_projects: [
      { project_id: 10, project: 'alpha', owners_count: 0, owners: [] }
    ]
  },
  release_trains: [
    {
      id: 500,
      workspace_id: 1,
      project_id: 10,
      title: 'Weekly Train',
      event_type: 'release',
      status: 'planned',
      start_at: '2026-02-19T09:00:00Z',
      end_at: '2026-02-19T11:00:00Z',
      notes: null,
      created_at: '2026-02-19T08:00:00Z',
      updated_at: '2026-02-19T08:00:00Z'
    }
  ],
  postmortems: [
    {
      id: 321,
      workspace_id: 1,
      incident_link_id: 901,
      title: 'alpha outage',
      summary: 'summary',
      root_cause: null,
      impact: null,
      action_items: ['stabilize flaky smoke test'],
      status: 'draft',
      created_at: '2026-02-20T12:00:00Z',
      updated_at: '2026-02-20T12:00:00Z'
    },
    {
      id: 322,
      workspace_id: 1,
      incident_link_id: null,
      title: 'beta outage',
      summary: 'summary',
      root_cause: null,
      impact: null,
      action_items: [],
      status: 'closed',
      created_at: '2026-02-19T12:00:00Z',
      updated_at: '2026-02-19T12:00:00Z'
    }
  ],
  slo_budgets: [
    {
      id: 1,
      workspace_id: 1,
      project_id: 10,
      service_name: 'alpha-api',
      slo_target_pct: 99.9,
      window_days: 30,
      error_budget_remaining_pct: 20,
      availability_pct: 99.1,
      burn_rate: 2.1,
      status: 'exhausted',
      created_at: null,
      updated_at: null
    }
  ]
} as unknown as OpsOverviewResponse;

describe('quality-hub insights', () => {
  it('builds release risk scores with weighted factors', () => {
    const result = buildReleaseRiskScoreboard({
      riskRadar: riskRadarFixture,
      opsOverview: opsOverviewFixture
    });

    expect(result.length).toBeGreaterThan(0);
    expect(result[0]?.project).toBe('alpha');
    expect(result[0]?.factors.open_incidents).toBe(1);
    expect(result[0]?.factors.ownership_gap).toBe(true);
  });

  it('builds forecast and improves outlook when trend rises', () => {
    const forecast = buildDoraForecast({
      doraMetrics: doraFixture,
      riskRadar: riskRadarFixture,
      horizonWeeks: 2
    });

    expect(forecast).not.toBeNull();
    expect(forecast?.outlook).toBe('improving');
    expect(forecast?.projected_deployments_per_week).toBeGreaterThan(
      doraFixture.deployment_frequency.per_week
    );
  });

  it('detects anomalies for elevated CFR and flakiness', () => {
    const anomalies = detectDoraAnomalies({
      doraMetrics: doraFixture,
      riskRadar: riskRadarFixture,
      opsOverview: opsOverviewFixture
    });

    expect(anomalies.some((item) => item.id === 'change-failure-spike')).toBe(
      true
    );
    expect(anomalies.some((item) => item.id === 'flaky-test-burst')).toBe(true);
  });

  it('simulates quality gate outcomes based on thresholds', () => {
    const simulation = simulateQualityGate({
      riskRadar: riskRadarFixture,
      opsOverview: opsOverviewFixture,
      thresholds: {
        max_release_risk_score: 60,
        min_release_readiness_pct: 75,
        min_delivery_confidence_pct: 70,
        block_on_open_incidents: true
      }
    });

    expect(simulation.summary.projects_total).toBe(2);
    expect(simulation.summary.blocked).toBeGreaterThan(0);
    expect(
      simulation.decisions.find((item) => item.project_id === 10)?.status
    ).toBe('blocked');
  });

  it('links incidents to deployments and prepares retro actions', () => {
    const links = buildIncidentDeploymentLinks({
      riskRadar: riskRadarFixture,
      opsOverview: opsOverviewFixture
    });
    const retro = buildRetroActionTracker({
      opsOverview: opsOverviewFixture
    });

    expect(links[0]?.incident_external_id).toBe('INC-901');
    expect(links[0]?.link_health).toBe('critical');
    expect(retro.length).toBe(2);
    expect(retro.some((item) => item.status === 'done')).toBe(true);
  });
});
