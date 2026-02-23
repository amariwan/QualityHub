import {
  DoraMetrics,
  OpsOverviewResponse,
  RiskRadarResponse
} from '@/features/quality-hub/types';

type RiskLevel = 'low' | 'medium' | 'high';
type Severity = 'low' | 'medium' | 'high';
type TeamStatus = 'green' | 'yellow' | 'red';

export type ReleaseRiskScoreItem = {
  project_id: number;
  project: string;
  score: number;
  level: RiskLevel;
  factors: {
    base_risk_score: number;
    test_failure_signals: number;
    open_incidents: number;
    hotfix_history_signals: number;
    ownership_gap: boolean;
  };
};

export type DoraForecast = {
  horizon_weeks: number;
  confidence_pct: number;
  outlook: 'improving' | 'steady' | 'degrading';
  projected_deployments_per_week: number;
  projected_lead_time_hours: number | null;
  projected_change_failure_rate_pct: number;
  projected_mttr_hours: number | null;
};

export type DoraAnomaly = {
  id: string;
  title: string;
  severity: Severity;
  description: string;
  recommendation: string;
};

export type TeamHeatmapItem = {
  team_id: number;
  team: string;
  team_status: TeamStatus;
  load_pct: number;
  project_count: number;
  quality_label: string;
};

export type FlakyTestRadarItem = {
  project_id: number;
  project: string;
  flakiness_score_pct: number;
  delivery_confidence_pct: number;
  mttr_hours: number | null;
  severity: Severity;
};

export type QualityGateThresholds = {
  max_release_risk_score: number;
  min_release_readiness_pct: number;
  min_delivery_confidence_pct: number;
  block_on_open_incidents: boolean;
};

export type QualityGateDecision = {
  project_id: number;
  project: string;
  status: 'blocked' | 'warning' | 'pass';
  release_risk_score: number;
  release_readiness_pct: number;
  delivery_confidence_pct: number;
  open_incidents: number;
  blocking_reasons: string[];
  warning_reasons: string[];
};

export type QualityGateSimulation = {
  thresholds: QualityGateThresholds;
  summary: {
    projects_total: number;
    blocked: number;
    warning: number;
    pass: number;
    simulated_release_success_rate_pct: number;
  };
  decisions: QualityGateDecision[];
};

export type IncidentDeploymentLink = {
  incident_id: number;
  incident_external_id: string;
  project_id: number;
  project: string;
  incident_status: string;
  linked_pipeline: string | null;
  linked_release_train: string | null;
  release_risk_level: RiskLevel;
  link_health: 'linked' | 'partial' | 'unlinked' | 'critical';
};

export type RetroActionItem = {
  id: string;
  postmortem_id: number;
  postmortem_title: string;
  title: string;
  status: 'open' | 'done';
  updated_at: string | null;
};

type ReleaseTrainRow = OpsOverviewResponse['release_trains'][number];

const DEFAULT_THRESHOLDS: QualityGateThresholds = {
  max_release_risk_score: 60,
  min_release_readiness_pct: 75,
  min_delivery_confidence_pct: 70,
  block_on_open_incidents: true
};

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function round(value: number, digits = 1) {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function projectLabel(project: string | null | undefined, projectId: number) {
  return project || `Project ${projectId}`;
}

function riskLevelFromScore(score: number): RiskLevel {
  if (score >= 70) return 'high';
  if (score >= 40) return 'medium';
  return 'low';
}

function severityFromScore(score: number): Severity {
  if (score >= 70) return 'high';
  if (score >= 35) return 'medium';
  return 'low';
}

export function buildReleaseRiskScoreboard(input: {
  riskRadar?: RiskRadarResponse;
  opsOverview?: OpsOverviewResponse;
}): ReleaseRiskScoreItem[] {
  const { riskRadar, opsOverview } = input;
  if (!riskRadar) return [];

  const regressionsByProject = new Map<number, number>();
  const testSignalsByProject = new Map<number, number>();
  for (const item of riskRadar.regressions) {
    const current = regressionsByProject.get(item.project_id) ?? 0;
    regressionsByProject.set(item.project_id, current + 1);
    if (
      item.type === 'test_failures' ||
      /flaky|test/i.test(item.reason || '')
    ) {
      const testCurrent = testSignalsByProject.get(item.project_id) ?? 0;
      testSignalsByProject.set(item.project_id, testCurrent + 1);
    }
  }

  const openIncidentsByProject = new Map<number, number>();
  for (const item of opsOverview?.incident_links ?? []) {
    if (item.status === 'resolved') continue;
    const current = openIncidentsByProject.get(item.project_id) ?? 0;
    openIncidentsByProject.set(item.project_id, current + 1);
  }

  const hotfixSignalsByProject = new Map<number, number>();
  for (const note of riskRadar.release_notes.feed) {
    if (!/bug|hotfix|security/i.test(note.category || note.category_label)) {
      continue;
    }
    const projectRisk = riskRadar.release_risk.projects.find(
      (row) => row.project === note.project
    );
    if (!projectRisk) continue;
    const current = hotfixSignalsByProject.get(projectRisk.project_id) ?? 0;
    hotfixSignalsByProject.set(projectRisk.project_id, current + 1);
  }

  const unownedProjects = new Set<number>(
    opsOverview?.ownership_heatmap.unowned_projects.map(
      (item) => item.project_id
    ) ?? []
  );

  return riskRadar.release_risk.projects
    .map((item) => {
      const testSignals = testSignalsByProject.get(item.project_id) ?? 0;
      const regressions = regressionsByProject.get(item.project_id) ?? 0;
      const openIncidents = openIncidentsByProject.get(item.project_id) ?? 0;
      const hotfixSignals = hotfixSignalsByProject.get(item.project_id) ?? 0;
      const ownershipGap = unownedProjects.has(item.project_id);

      const score = clamp(
        item.score * 0.55 +
          regressions * 7 +
          testSignals * 4 +
          openIncidents * 12 +
          hotfixSignals * 6 +
          (ownershipGap ? 10 : 0),
        0,
        100
      );

      return {
        project_id: item.project_id,
        project: projectLabel(item.project, item.project_id),
        score: round(score, 1),
        level: riskLevelFromScore(score),
        factors: {
          base_risk_score: round(item.score, 1),
          test_failure_signals: testSignals,
          open_incidents: openIncidents,
          hotfix_history_signals: hotfixSignals,
          ownership_gap: ownershipGap
        }
      };
    })
    .sort((a, b) => b.score - a.score);
}

export function buildDoraForecast(input: {
  doraMetrics?: DoraMetrics;
  riskRadar?: RiskRadarResponse;
  horizonWeeks?: number;
}): DoraForecast | null {
  const { doraMetrics, riskRadar } = input;
  if (!doraMetrics) return null;

  const horizonWeeks = input.horizonWeeks ?? 2;
  const trend = riskRadar?.quality_trend ?? [];
  const slope =
    trend.length >= 2
      ? (trend[trend.length - 1].score - trend[0].score) / (trend.length - 1)
      : 0;
  const normalizedSlope = clamp(slope / 15, -0.35, 0.35);

  const deploymentMultiplier = clamp(1 + normalizedSlope * 0.8, 0.55, 1.45);
  const reliabilityMultiplier = clamp(1 - normalizedSlope * 0.6, 0.55, 1.45);

  const confidenceBase = Math.min(1, doraMetrics.sample_size / 90);
  const confidenceTrendFactor = trend.length >= 4 ? 1 : 0.82;
  const confidencePct = round(
    clamp(confidenceBase * confidenceTrendFactor, 0.2, 0.97) * 100,
    1
  );

  return {
    horizon_weeks: horizonWeeks,
    confidence_pct: confidencePct,
    outlook:
      normalizedSlope > 0.08
        ? 'improving'
        : normalizedSlope < -0.08
          ? 'degrading'
          : 'steady',
    projected_deployments_per_week: round(
      doraMetrics.deployment_frequency.per_week * deploymentMultiplier,
      2
    ),
    projected_lead_time_hours:
      doraMetrics.lead_time_hours.value === null
        ? null
        : round(
            Math.max(
              0.1,
              doraMetrics.lead_time_hours.value * reliabilityMultiplier
            ),
            1
          ),
    projected_change_failure_rate_pct: round(
      clamp(
        doraMetrics.change_failure_rate.pct * reliabilityMultiplier,
        0,
        100
      ),
      1
    ),
    projected_mttr_hours:
      doraMetrics.mttr_hours.value === null
        ? null
        : round(
            Math.max(0.1, doraMetrics.mttr_hours.value * reliabilityMultiplier),
            1
          )
  };
}

export function detectDoraAnomalies(input: {
  doraMetrics?: DoraMetrics;
  riskRadar?: RiskRadarResponse;
  opsOverview?: OpsOverviewResponse;
}): DoraAnomaly[] {
  const { doraMetrics, riskRadar, opsOverview } = input;
  if (!doraMetrics) return [];

  const anomalies: DoraAnomaly[] = [];
  const openIncidents =
    opsOverview?.incident_links.filter((item) => item.status !== 'resolved')
      .length ?? 0;

  if (doraMetrics.change_failure_rate.pct >= 15) {
    anomalies.push({
      id: 'change-failure-spike',
      title: 'Change Failure Rate spike',
      severity: 'high',
      description: `${round(doraMetrics.change_failure_rate.pct, 1)}% CFR is above the high-risk threshold.`,
      recommendation:
        'Inspect recent deployments, rollback causes, and enforce stricter release gates.'
    });
  }

  if (
    doraMetrics.lead_time_hours.value !== null &&
    doraMetrics.lead_time_hours.value >= 72
  ) {
    anomalies.push({
      id: 'lead-time-drift',
      title: 'Lead time drift detected',
      severity: 'medium',
      description: `Lead time is ${round(doraMetrics.lead_time_hours.value, 1)}h, indicating slower delivery flow.`,
      recommendation:
        'Review review-cycle bottlenecks and long-running pipeline stages.'
    });
  }

  const trend = riskRadar?.quality_trend ?? [];
  if (trend.length >= 4) {
    const latest = trend[trend.length - 1]?.score ?? 0;
    const baseline =
      trend.slice(0, -1).reduce((sum, item) => sum + item.score, 0) /
      (trend.length - 1);
    const drop = baseline - latest;
    if (drop >= 8) {
      anomalies.push({
        id: 'quality-trend-drop',
        title: 'Quality trend dropped',
        severity: drop >= 15 ? 'high' : 'medium',
        description: `Latest trend score is ${round(latest, 1)} vs baseline ${round(baseline, 1)}.`,
        recommendation:
          'Prioritize high-severity regressions and stabilize failing services before next release.'
      });
    }
  }

  if (doraMetrics.deployment_frequency.deployments > 0) {
    const incidentRate =
      openIncidents / Math.max(1, doraMetrics.deployment_frequency.deployments);
    if (incidentRate >= 0.2) {
      anomalies.push({
        id: 'incident-load',
        title: 'Incident load is elevated',
        severity: incidentRate >= 0.35 ? 'high' : 'medium',
        description: `${openIncidents} open incidents for ${doraMetrics.deployment_frequency.deployments} deployments in the current window.`,
        recommendation:
          'Freeze risky releases temporarily and resolve incident backlog.'
      });
    }
  }

  const flakyProjects = (riskRadar?.delivery_confidence ?? []).filter(
    (item) => item.flakiness_score_pct >= 35
  );
  if (flakyProjects.length > 0) {
    anomalies.push({
      id: 'flaky-test-burst',
      title: 'Flaky test burst',
      severity: flakyProjects.length >= 4 ? 'high' : 'medium',
      description: `${flakyProjects.length} projects exceed 35% flakiness score.`,
      recommendation:
        'Quarantine unstable test suites and reduce merge queue pressure.'
    });
  }

  return anomalies.sort((a, b) => {
    const severityRank: Record<Severity, number> = {
      high: 3,
      medium: 2,
      low: 1
    };
    return severityRank[b.severity] - severityRank[a.severity];
  });
}

export function buildTeamHeatmap(input: {
  opsOverview?: OpsOverviewResponse;
  riskRadar?: RiskRadarResponse;
}): TeamHeatmapItem[] {
  const { opsOverview, riskRadar } = input;
  if (!opsOverview) return [];

  const qualityByTeam = new Map(
    (riskRadar?.team_quality_indicator ?? []).map((item) => [
      item.team.toLowerCase(),
      item
    ])
  );

  return opsOverview.ownership_heatmap.teams
    .map((item) => {
      const loadPct =
        item.capacity_threshold > 0
          ? (item.project_count / item.capacity_threshold) * 100
          : 0;
      const quality = qualityByTeam.get(item.team.toLowerCase());

      let teamStatus: TeamStatus;
      if (quality?.stability) {
        teamStatus = quality.stability;
      } else if (item.status === 'overloaded') {
        teamStatus = 'red';
      } else if (item.status === 'balanced') {
        teamStatus = 'yellow';
      } else {
        teamStatus = 'green';
      }

      return {
        team_id: item.team_id,
        team: item.team,
        team_status: teamStatus,
        load_pct: round(loadPct, 1),
        project_count: item.project_count,
        quality_label: quality?.label ?? item.status
      };
    })
    .sort((a, b) => b.load_pct - a.load_pct);
}

export function buildFlakyTestRadar(
  riskRadar?: RiskRadarResponse
): FlakyTestRadarItem[] {
  if (!riskRadar) return [];

  return riskRadar.delivery_confidence
    .map((item) => ({
      project_id: item.project_id,
      project: projectLabel(item.project, item.project_id),
      flakiness_score_pct: round(item.flakiness_score_pct, 1),
      delivery_confidence_pct: round(item.value_pct, 1),
      mttr_hours: item.mttr_hours,
      severity: severityFromScore(item.flakiness_score_pct)
    }))
    .filter((item) => item.flakiness_score_pct > 0)
    .sort((a, b) => b.flakiness_score_pct - a.flakiness_score_pct);
}

export function simulateQualityGate(input: {
  riskRadar?: RiskRadarResponse;
  opsOverview?: OpsOverviewResponse;
  thresholds?: Partial<QualityGateThresholds>;
}): QualityGateSimulation {
  const thresholds: QualityGateThresholds = {
    ...DEFAULT_THRESHOLDS,
    ...(input.thresholds || {})
  };

  if (!input.riskRadar) {
    return {
      thresholds,
      summary: {
        projects_total: 0,
        blocked: 0,
        warning: 0,
        pass: 0,
        simulated_release_success_rate_pct: 0
      },
      decisions: []
    };
  }

  const releaseReadinessByProject = new Map(
    input.riskRadar.release_readiness.map((item) => [item.project_id, item])
  );
  const confidenceByProject = new Map(
    input.riskRadar.delivery_confidence.map((item) => [item.project_id, item])
  );
  const openIncidentsByProject = new Map<number, number>();
  for (const incident of input.opsOverview?.incident_links ?? []) {
    if (incident.status === 'resolved') continue;
    const current = openIncidentsByProject.get(incident.project_id) ?? 0;
    openIncidentsByProject.set(incident.project_id, current + 1);
  }

  const decisions: QualityGateDecision[] = input.riskRadar.release_risk.projects
    .map<QualityGateDecision>((projectRisk) => {
      const readiness =
        releaseReadinessByProject.get(projectRisk.project_id)?.value_pct ?? 0;
      const confidence =
        confidenceByProject.get(projectRisk.project_id)?.value_pct ?? 0;
      const openIncidents =
        openIncidentsByProject.get(projectRisk.project_id) ?? 0;

      const blockingReasons: string[] = [];
      const warningReasons: string[] = [];

      if (projectRisk.score > thresholds.max_release_risk_score) {
        blockingReasons.push('release risk above threshold');
      } else if (projectRisk.score > thresholds.max_release_risk_score * 0.8) {
        warningReasons.push('release risk close to threshold');
      }

      if (readiness < thresholds.min_release_readiness_pct) {
        blockingReasons.push('release readiness below minimum');
      } else if (readiness < thresholds.min_release_readiness_pct + 5) {
        warningReasons.push('release readiness near minimum');
      }

      if (confidence < thresholds.min_delivery_confidence_pct) {
        blockingReasons.push('delivery confidence below minimum');
      } else if (confidence < thresholds.min_delivery_confidence_pct + 5) {
        warningReasons.push('delivery confidence near minimum');
      }

      if (thresholds.block_on_open_incidents && openIncidents > 0) {
        blockingReasons.push('open incidents linked to project');
      }

      const status: QualityGateDecision['status'] =
        blockingReasons.length > 0
          ? 'blocked'
          : warningReasons.length > 0
            ? 'warning'
            : 'pass';

      return {
        project_id: projectRisk.project_id,
        project: projectLabel(projectRisk.project, projectRisk.project_id),
        status,
        release_risk_score: round(projectRisk.score, 1),
        release_readiness_pct: round(readiness, 1),
        delivery_confidence_pct: round(confidence, 1),
        open_incidents: openIncidents,
        blocking_reasons: blockingReasons,
        warning_reasons: warningReasons
      };
    })
    .sort((a, b) => {
      const statusRank: Record<QualityGateDecision['status'], number> = {
        blocked: 3,
        warning: 2,
        pass: 1
      };
      return statusRank[b.status] - statusRank[a.status];
    });

  const blocked = decisions.filter((item) => item.status === 'blocked').length;
  const warning = decisions.filter((item) => item.status === 'warning').length;
  const pass = decisions.filter((item) => item.status === 'pass').length;
  const projectsTotal = decisions.length;

  return {
    thresholds,
    summary: {
      projects_total: projectsTotal,
      blocked,
      warning,
      pass,
      simulated_release_success_rate_pct:
        projectsTotal === 0 ? 0 : round((pass / projectsTotal) * 100, 1)
    },
    decisions
  };
}

export function buildIncidentDeploymentLinks(input: {
  opsOverview?: OpsOverviewResponse;
  riskRadar?: RiskRadarResponse;
}): IncidentDeploymentLink[] {
  const { opsOverview, riskRadar } = input;
  if (!opsOverview) return [];

  const riskByProject = new Map(
    (riskRadar?.release_risk.projects ?? []).map((item) => [
      item.project_id,
      item
    ])
  );

  const releaseTrainsByProject = new Map<number, ReleaseTrainRow[]>();
  for (const item of opsOverview.release_trains) {
    if (!item.project_id) continue;
    const current = releaseTrainsByProject.get(item.project_id) ?? [];
    current.push(item);
    releaseTrainsByProject.set(item.project_id, current);
  }

  Array.from(releaseTrainsByProject.entries()).forEach(([projectId, rows]) => {
    rows.sort((a: ReleaseTrainRow, b: ReleaseTrainRow) => {
      const aTime = new Date(a.start_at || 0).getTime();
      const bTime = new Date(b.start_at || 0).getTime();
      return bTime - aTime;
    });
    releaseTrainsByProject.set(projectId, rows);
  });

  return opsOverview.incident_links
    .map((item) => {
      const risk = riskByProject.get(item.project_id);
      const latestReleaseTrain = releaseTrainsByProject.get(
        item.project_id
      )?.[0];
      const releaseRiskLevel = risk?.level ?? 'medium';
      const pipelineLabel = item.gitlab_pipeline_id
        ? `#${item.gitlab_pipeline_id}`
        : item.pipeline_id
          ? `pipeline:${item.pipeline_id}`
          : null;
      const releaseTrainLabel = latestReleaseTrain
        ? `${latestReleaseTrain.title} (${latestReleaseTrain.status})`
        : null;

      let linkHealth: IncidentDeploymentLink['link_health'] = 'linked';
      if (!pipelineLabel && !releaseTrainLabel) {
        linkHealth = 'unlinked';
      } else if (!pipelineLabel || !releaseTrainLabel) {
        linkHealth = 'partial';
      }
      if (item.status !== 'resolved' && releaseRiskLevel === 'high') {
        linkHealth = 'critical';
      }

      return {
        incident_id: item.id,
        incident_external_id: item.external_issue_id,
        project_id: item.project_id,
        project: projectLabel(item.project, item.project_id),
        incident_status: item.status,
        linked_pipeline: pipelineLabel,
        linked_release_train: releaseTrainLabel,
        release_risk_level: releaseRiskLevel,
        link_health: linkHealth
      };
    })
    .sort((a, b) => {
      const statusRank = (value: string) => {
        if (value !== 'resolved') return 2;
        return 1;
      };
      return statusRank(b.incident_status) - statusRank(a.incident_status);
    });
}

export function buildRetroActionTracker(input: {
  opsOverview?: OpsOverviewResponse;
}): RetroActionItem[] {
  const postmortems = input.opsOverview?.postmortems ?? [];

  const actions = postmortems.flatMap((postmortem) => {
    const rows =
      postmortem.action_items.length > 0
        ? postmortem.action_items
        : [`Follow-up on "${postmortem.title}"`];

    return rows.map<RetroActionItem>((title, index) => {
      const status: RetroActionItem['status'] =
        postmortem.status === 'closed' || postmortem.status === 'published'
          ? 'done'
          : 'open';
      return {
        id: `${postmortem.id}:${index}`,
        postmortem_id: postmortem.id,
        postmortem_title: postmortem.title,
        title,
        status,
        updated_at: postmortem.updated_at
      };
    });
  });

  return actions.sort((a, b) => {
    if (a.status !== b.status) {
      return a.status === 'open' ? -1 : 1;
    }
    const aTime = new Date(a.updated_at || 0).getTime();
    const bTime = new Date(b.updated_at || 0).getTime();
    return bTime - aTime;
  });
}
