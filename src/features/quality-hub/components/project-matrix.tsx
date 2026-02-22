'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { getProjectMatrix } from '@/features/quality-hub/api/client';
import { ProjectMatrixResponse } from '@/features/quality-hub/types';
import { useEffect, useState } from 'react';

export function ProjectMatrix({ projectId }: { projectId: number }) {
  const [data, setData] = useState<ProjectMatrixResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        setError(null);
        const result = await getProjectMatrix(projectId);
        setData(result);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : 'Failed to load project matrix'
        );
      } finally {
        setLoading(false);
      }
    }

    void loadData();
  }, [projectId]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Project {projectId} Deployment Matrix</CardTitle>
      </CardHeader>
      <CardContent>
        {loading && (
          <p className='text-muted-foreground text-sm'>Loading matrix...</p>
        )}
        {error && <p className='text-destructive text-sm'>{error}</p>}
        {!loading && !error && data && (
          <div className='space-y-3'>
            {Object.keys(data.matrix).length === 0 && (
              <p className='text-muted-foreground text-sm'>
                No deployment rows found for this project.
              </p>
            )}
            {Object.entries(data.matrix).map(([env, rows]) => (
              <div key={env} className='rounded-md border p-3'>
                <h4 className='font-medium capitalize'>{env}</h4>
                <div className='mt-2 space-y-2'>
                  {rows.map((row) => (
                    <div key={String(row.deployment_id)} className='text-sm'>
                      <span className='font-medium'>{String(row.status)}</span>
                      {' · '}
                      {String(row.kind)} / {String(row.namespace)} /{' '}
                      {String(row.resource_name)}
                      {' · '}
                      revision: {String(row.git_revision || '-')}
                      {' · '}
                      tag: {String(row.git_tag || '-')}
                      {' · '}
                      image: {String(row.image_ref || '-')}
                      {' · '}
                      chart: {String(row.helm_chart_version || '-')}
                      {' · '}
                      actor:{' '}
                      {String(row.actor_merger || row.actor_author || '-')}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
