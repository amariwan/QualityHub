'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { getPipelines } from '@/features/quality-hub/api/client';
import { PipelineItem } from '@/features/quality-hub/types';
import { useCallback, useEffect, useState } from 'react';

export function PipelinesTable() {
  const [scope, setScope] = useState<'all' | 'readiness'>('readiness');
  const [items, setItems] = useState<PipelineItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async (nextScope: 'all' | 'readiness') => {
    try {
      setLoading(true);
      setError(null);
      const data = await getPipelines(nextScope);
      setItems(data.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load pipelines');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadData(scope);
  }, [loadData, scope]);

  return (
    <Card>
      <CardHeader className='flex flex-row items-center justify-between'>
        <CardTitle>Broken Pipelines</CardTitle>
        <div className='flex gap-2'>
          <Button
            variant={scope === 'readiness' ? 'default' : 'outline'}
            onClick={async () => {
              setScope('readiness');
              await loadData('readiness');
            }}
          >
            Readiness
          </Button>
          <Button
            variant={scope === 'all' ? 'default' : 'outline'}
            onClick={async () => {
              setScope('all');
              await loadData('all');
            }}
          >
            All
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {loading && (
          <p className='text-muted-foreground text-sm'>Loading pipelines...</p>
        )}
        {error && <p className='text-destructive text-sm'>{error}</p>}
        {!loading && !error && (
          <div className='space-y-2'>
            {items.length === 0 && (
              <p className='text-muted-foreground text-sm'>
                No broken pipelines for this scope.
              </p>
            )}
            {items.map((item) => (
              <div key={item.id} className='rounded-md border p-3'>
                <div className='flex flex-wrap items-center gap-2'>
                  <Badge variant='outline'>Project {item.project_id}</Badge>
                  <Badge>{item.status}</Badge>
                  <Badge variant='secondary'>{item.deployability_state}</Badge>
                  <span className='text-muted-foreground text-xs'>
                    #{item.gitlab_pipeline_id}
                  </span>
                </div>
                <p className='text-muted-foreground mt-2 text-xs'>
                  ref: {item.ref || '-'} | sha: {item.sha || '-'} | source:{' '}
                  {item.source_type || '-'}
                </p>
                {item.failure_reasons.length > 0 && (
                  <p className='mt-2 text-xs'>
                    Reasons: {item.failure_reasons.join(', ')}
                  </p>
                )}
                {item.missing_signals.length > 0 && (
                  <p className='mt-1 text-xs text-amber-700'>
                    Missing signals: {item.missing_signals.join(', ')}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
