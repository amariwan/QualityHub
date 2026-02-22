'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import {
  createWorkspaceView,
  listWorkspaceViews
} from '@/features/quality-hub/api/client';
import { useEffect, useState } from 'react';

export function WorkspaceViewsManager() {
  const [name, setName] = useState('');
  const [items, setItems] = useState<
    Array<{ id: number; name: string; visibility: string }>
  >([]);
  const [error, setError] = useState<string | null>(null);

  async function loadItems() {
    try {
      setError(null);
      const data = await listWorkspaceViews();
      setItems(
        data.map((item) => ({
          id: item.id,
          name: item.name,
          visibility: item.visibility
        }))
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load views');
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
            placeholder='View name'
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
          <Button
            onClick={async () => {
              if (!name.trim()) return;
              await createWorkspaceView({
                name: name.trim(),
                definition_json: {}
              });
              setName('');
              await loadItems();
            }}
          >
            Add View
          </Button>
        </div>
        {error && <p className='text-destructive text-sm'>{error}</p>}
        <div className='space-y-1'>
          {items.map((item) => (
            <p key={item.id} className='text-sm'>
              #{item.id} {item.name} ({item.visibility})
            </p>
          ))}
          {items.length === 0 && (
            <p className='text-muted-foreground text-sm'>No saved views.</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
