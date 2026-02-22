'use client';

import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

const STATUS_CLASS: Record<string, string> = {
  ready: 'bg-emerald-500/10 text-emerald-700 border-emerald-500/30',
  progressing: 'bg-amber-500/10 text-amber-700 border-amber-500/30',
  degraded: 'bg-orange-500/10 text-orange-700 border-orange-500/30',
  failed: 'bg-red-500/10 text-red-700 border-red-500/30',
  unknown: 'bg-slate-500/10 text-slate-700 border-slate-500/30'
};

export function EnvStatusChip({
  label,
  status
}: {
  label: string;
  status: string;
}) {
  return (
    <Badge
      variant='outline'
      className={cn('capitalize', STATUS_CLASS[status] || '')}
    >
      {label}: {status}
    </Badge>
  );
}
