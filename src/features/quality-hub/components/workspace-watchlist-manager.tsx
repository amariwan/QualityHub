'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import {
  createWorkspaceWatchlist,
  listWorkspaceWatchlist
} from '@/features/quality-hub/api/client';
import { useEffect, useState } from 'react';

export function WorkspaceWatchlistManager() {
  const [projectId, setProjectId] = useState('');
  const [items, setItems] = useState<
    Array<{ id: number; project_id: number; visibility: string }>
  >([]);
  const [error, setError] = useState<string | null>(null);

  async function loadItems() {
    try {
      setError(null);
      const data = await listWorkspaceWatchlist();
      setItems(
        data.map((item) => ({
          id: item.id,
          project_id: item.project_id,
          visibility: item.visibility
        }))
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load watchlist');
    }
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void loadItems();
  }, []);

  return (
    <Card>
      <CardContent className='space-y-3 pt-6'>
        <div className='flex gap-2'>
          <Input
            placeholder='Project ID'
            value={projectId}
            onChange={(event) => setProjectId(event.target.value)}
          />
          <Button
            onClick={async () => {
              if (!projectId.trim()) return;
              await createWorkspaceWatchlist({ project_id: Number(projectId) });
              setProjectId('');
              await loadItems();
            }}
          >
            Add Watch
          </Button>
        </div>
        {error && <p className='text-destructive text-sm'>{error}</p>}
        <div className='space-y-1'>
          {items.map((item) => (
            <p key={item.id} className='text-sm'>
              #{item.id} project {item.project_id} ({item.visibility})
            </p>
          ))}
          {items.length === 0 && (
            <p className='text-muted-foreground text-sm'>
              No watchlist entries.
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
