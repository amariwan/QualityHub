import { NavItem } from '@/types';

export const navItems: NavItem[] = [
  {
    title: 'Portfolio',
    url: '/dashboard/quality-hub/portfolio',
    icon: 'dashboard',
    isActive: true,
    items: []
  },
  {
    title: 'Pipelines',
    url: '/dashboard/quality-hub/pipelines',
    icon: 'warning',
    isActive: false,
    items: []
  },
  {
    title: 'Workspace',
    url: '#',
    icon: 'workspace',
    isActive: false,
    items: [
      {
        title: 'Views',
        url: '/dashboard/quality-hub/workspace/views'
      },
      {
        title: 'Notes',
        url: '/dashboard/quality-hub/workspace/notes'
      },
      {
        title: 'Watchlist',
        url: '/dashboard/quality-hub/workspace/watchlist'
      },
      {
        title: 'Tags',
        url: '/dashboard/quality-hub/workspace/tags'
      },
      {
        title: 'Teams',
        url: '/dashboard/quality-hub/workspace/teams'
      }
    ]
  }
];
