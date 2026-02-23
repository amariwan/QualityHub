import PageContainer from '@/components/layout/page-container';
import { Badge } from '@/components/ui/badge';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardAction,
  CardFooter
} from '@/components/ui/card';
import { IconTrendingDown, IconTrendingUp } from '@tabler/icons-react';
import React from 'react';

export default function OverViewLayout({
  children
}: {
  children: React.ReactNode;
}) {
  // we no longer provide parallel-route slots; the page itself renders all stats
  return <PageContainer>{children}</PageContainer>;
}
