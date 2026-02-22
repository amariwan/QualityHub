'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import {
  createWorkspaceNote,
  listWorkspaceNotes
} from '@/features/quality-hub/api/client';
import { useEffect, useState } from 'react';

export function WorkspaceNotesManager() {
  const [content, setContent] = useState('');
  const [items, setItems] = useState<
    Array<{ id: number; content: string; scope_type: string }>
  >([]);
  const [error, setError] = useState<string | null>(null);

  async function loadItems() {
    try {
      setError(null);
      const data = await listWorkspaceNotes();
      setItems(
        data.map((item) => ({
          id: item.id,
          content: item.content,
          scope_type: item.scope_type
        }))
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load notes');
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
            placeholder='Note content'
            value={content}
            onChange={(event) => setContent(event.target.value)}
          />
          <Button
            onClick={async () => {
              if (!content.trim()) return;
              await createWorkspaceNote({ content: content.trim() });
              setContent('');
              await loadItems();
            }}
          >
            Add Note
          </Button>
        </div>
        {error && <p className='text-destructive text-sm'>{error}</p>}
        <div className='space-y-1'>
          {items.map((item) => (
            <p key={item.id} className='text-sm'>
              #{item.id} [{item.scope_type}] {item.content}
            </p>
          ))}
          {items.length === 0 && (
            <p className='text-muted-foreground text-sm'>No notes.</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
