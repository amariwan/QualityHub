import {
  createOpsProductEvent,
  listOpsProductEvents
} from '@/features/quality-hub/api/client';
import {
  OpsOverviewResponse,
  OpsProductEvent,
  OpsProductEventName
} from '@/features/quality-hub/types';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import useSWR from 'swr';
import {
  OPS_EVENT_SCENARIO_BY_NAME,
  OPS_EVENT_TODOS
} from './ops-center-events';

type UseOpsProductEventsParams = {
  workspaceId: number | null | undefined;
  weeks: number;
  days: number;
  data: OpsOverviewResponse | undefined;
};

export function useOpsProductEvents({
  workspaceId,
  weeks,
  days,
  data
}: UseOpsProductEventsParams) {
  const [eventActionWorking, setEventActionWorking] = useState(false);
  const [eventActionError, setEventActionError] = useState<string | null>(null);
  const autoTrackedRef = useRef<Record<string, boolean>>({});
  const hadOpenIncidentsRef = useRef(false);
  const hadFlakySignalsRef = useRef(false);
  const hadSLOBreachRef = useRef(false);

  const { data: productEvents = [], mutate: mutateProductEvents } = useSWR(
    workspaceId === undefined
      ? null
      : ['quality-hub', 'ops-product-events', workspaceId ?? 'all'],
    () => listOpsProductEvents({ workspaceId, limit: 500 })
  );

  const trackProductEvent = useCallback(
    async (
      scenario: string,
      eventName: OpsProductEventName,
      metadataJson: Record<string, unknown> = {}
    ) => {
      await createOpsProductEvent({
        workspace_id: workspaceId,
        scenario,
        event_name: eventName,
        metadata_json: metadataJson
      });
      await mutateProductEvents();
    },
    [workspaceId, mutateProductEvents]
  );

  const runEventAction = useCallback(async (fn: () => Promise<unknown>) => {
    try {
      setEventActionWorking(true);
      setEventActionError(null);
      await fn();
    } catch (err) {
      setEventActionError(
        err instanceof Error ? err.message : 'Failed to track event'
      );
    } finally {
      setEventActionWorking(false);
    }
  }, []);

  const emitOpsEvent = useCallback(
    (
      eventName: OpsProductEventName,
      metadataJson: Record<string, unknown> = {}
    ) => {
      void trackProductEvent(
        OPS_EVENT_SCENARIO_BY_NAME[eventName],
        eventName,
        metadataJson
      ).catch(() => {
        // ignore telemetry write errors during background tracking
      });
    },
    [trackProductEvent]
  );

  const emitOpsEventOnce = useCallback(
    (
      guardKey: string,
      eventName: OpsProductEventName,
      metadataJson: Record<string, unknown> = {}
    ) => {
      if (autoTrackedRef.current[guardKey]) return;
      autoTrackedRef.current[guardKey] = true;
      emitOpsEvent(eventName, metadataJson);
    },
    [emitOpsEvent]
  );

  const openIncidentCount = useMemo(
    () =>
      data
        ? data.incident_links.filter((item) => item.status !== 'resolved')
            .length
        : 0,
    [data]
  );
  const highRiskProjectCount =
    data?.trend_regressions.summary.high_risk_projects ?? 0;
  const unownedProjectCount =
    data?.ownership_heatmap.summary.unowned_projects ?? 0;
  const regressionCount = data?.trend_regressions.regressions.length ?? 0;
  const flakyRegressionCount =
    data?.trend_regressions.regressions.filter(
      (item) =>
        item.type === 'test_failures' || /flaky|test/i.test(item.reason || '')
    ).length ?? 0;
  const breachedSLOCount =
    data?.slo_budgets.filter((item) => item.status === 'exhausted').length ?? 0;
  const mttrHours = data?.dora_metrics.mttr_hours.value ?? null;

  const latestProductEventByName = useMemo(() => {
    const mapped = new Map<string, OpsProductEvent>();
    for (const item of productEvents) {
      if (!mapped.has(item.event_name)) {
        mapped.set(item.event_name, item);
      }
    }
    return mapped;
  }, [productEvents]);

  const todoProgress = useMemo(
    () =>
      OPS_EVENT_TODOS.map((todo) => {
        const trackedCount = todo.events.filter((eventName) =>
          latestProductEventByName.has(eventName)
        ).length;
        return {
          ...todo,
          trackedCount,
          total: todo.events.length,
          done: trackedCount === todo.events.length
        };
      }),
    [latestProductEventByName]
  );

  useEffect(() => {
    autoTrackedRef.current = {};
    hadOpenIncidentsRef.current = false;
    hadFlakySignalsRef.current = false;
    hadSLOBreachRef.current = false;
  }, [workspaceId]);

  useEffect(() => {
    if (!data) return;
    emitOpsEventOnce('dashboard_opened', 'quality_dashboard_opened', {
      weeks,
      days
    });
  }, [data, days, emitOpsEventOnce, weeks]);

  useEffect(() => {
    if (!data || highRiskProjectCount <= 0) return;
    emitOpsEventOnce(
      'quality_score_threshold_breached',
      'quality_score_threshold_breached',
      {
        high_risk_projects: highRiskProjectCount
      }
    );
  }, [data, emitOpsEventOnce, highRiskProjectCount]);

  useEffect(() => {
    if (!data) return;
    emitOpsEventOnce('incident_timeline_opened', 'incident_timeline_opened', {
      open_incidents: openIncidentCount
    });
  }, [data, emitOpsEventOnce, openIncidentCount]);

  useEffect(() => {
    if (!data) return;
    emitOpsEventOnce('impact_heatmap_opened', 'impact_heatmap_opened', {
      unowned_projects: unownedProjectCount,
      overloaded_teams: data.ownership_heatmap.summary.overloaded_teams
    });
  }, [data, emitOpsEventOnce, unownedProjectCount]);

  useEffect(() => {
    if (!data || regressionCount <= 0) return;
    emitOpsEventOnce(
      'post_release_regression_detected',
      'post_release_regression_detected',
      {
        regressions: regressionCount
      }
    );
  }, [data, emitOpsEventOnce, regressionCount]);

  useEffect(() => {
    if (!data || regressionCount <= 0) return;
    emitOpsEventOnce('change_failure_detected', 'change_failure.detected', {
      regressions: regressionCount
    });
  }, [data, emitOpsEventOnce, regressionCount]);

  useEffect(() => {
    if (!data || mttrHours === null) return;
    emitOpsEventOnce('mttr_updated', 'mttr.updated', {
      mttr_hours: mttrHours
    });
  }, [data, emitOpsEventOnce, mttrHours]);

  useEffect(() => {
    if (!data || unownedProjectCount <= 0) return;
    emitOpsEventOnce('owner_missing_detected', 'owner_missing_detected', {
      unowned_projects: unownedProjectCount
    });
  }, [data, emitOpsEventOnce, unownedProjectCount]);

  useEffect(() => {
    if (!data || openIncidentCount <= 0 || highRiskProjectCount <= 0) return;
    emitOpsEventOnce('escalation_triggered', 'escalation_triggered', {
      open_incidents: openIncidentCount,
      high_risk_projects: highRiskProjectCount
    });
  }, [data, emitOpsEventOnce, highRiskProjectCount, openIncidentCount]);

  useEffect(() => {
    if (!data) return;
    if (openIncidentCount > 0) {
      hadOpenIncidentsRef.current = true;
      emitOpsEventOnce('incident_opened', 'incident.opened', {
        open_incidents: openIncidentCount
      });
      return;
    }
    if (hadOpenIncidentsRef.current) {
      emitOpsEventOnce('incident_resolved', 'incident.resolved', {
        resolved_incidents: data.incident_links.length
      });
    }
  }, [data, emitOpsEventOnce, openIncidentCount]);

  useEffect(() => {
    if (!data) return;
    if (flakyRegressionCount > 0) {
      hadFlakySignalsRef.current = true;
      emitOpsEventOnce('test_flaky_detected', 'test.flaky_detected', {
        flaky_signals: flakyRegressionCount
      });
      return;
    }
    if (hadFlakySignalsRef.current) {
      emitOpsEventOnce('test_flaky_resolved', 'test.flaky_resolved', {
        flaky_signals: 0
      });
    }
  }, [data, emitOpsEventOnce, flakyRegressionCount]);

  useEffect(() => {
    if (!data) return;
    if (breachedSLOCount > 0) {
      hadSLOBreachRef.current = true;
      emitOpsEventOnce('slo_breached', 'slo.breached', {
        breached_services: breachedSLOCount
      });
      return;
    }
    if (hadSLOBreachRef.current && data.slo_budgets.length > 0) {
      emitOpsEventOnce('slo_recovered', 'slo.recovered', {
        recovered_services: data.slo_budgets.length
      });
    }
  }, [data, emitOpsEventOnce, breachedSLOCount]);

  return {
    eventActionWorking,
    eventActionError,
    productEvents,
    openIncidentCount,
    highRiskProjectCount,
    emitOpsEvent,
    emitOpsEventOnce,
    runEventAction,
    todoProgress,
    latestProductEventByName,
    trackProductEvent
  };
}
