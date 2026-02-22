'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import {
  createWorkspaceTag,
  listWorkspaceTags
} from '@/features/quality-hub/api/client';
import { useEffect, useState } from 'react';

export function WorkspaceTagsManager() {
  const [name, setName] = useState('');
  const [color, setColor] = useState('#2563eb');
  const [items, setItems] = useState<
    Array<{ id: number; name: string; color: string | null }>
  >([]);
  const [error, setError] = useState<string | null>(null);

  async function loadItems() {
    try {
      setError(null);
      const data = await listWorkspaceTags();
      setItems(
        data.map((item) => ({
          id: item.id,
          name: item.name,
          color: item.color
        }))
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tags');
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
            placeholder='Tag name'
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
          <Input
            placeholder='Color'
            value={color}
            onChange={(event) => setColor(event.target.value)}
          />
          <Button
            onClick={async () => {
              if (!name.trim()) return;
              await createWorkspaceTag({ name: name.trim(), color });
              setName('');
              await loadItems();
            }}
          >
            Add Tag
          </Button>
        </div>
        {error && <p className='text-destructive text-sm'>{error}</p>}
        <div className='space-y-1'>
          {items.map((item) => (
            <p key={item.id} className='text-sm'>
              #{item.id} {item.name} ({item.color || 'no color'})
            </p>
          ))}
          {items.length === 0 && (
            <p className='text-muted-foreground text-sm'>No tags.</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
