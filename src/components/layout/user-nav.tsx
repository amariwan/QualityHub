'use client';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';
import { UserAvatarProfile } from '@/components/user-avatar-profile';
import { disconnectGitlabToken } from '@/features/quality-hub/api/client';
import { useRouter } from 'next/navigation';

export function UserNav() {
  const router = useRouter();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant='ghost' className='relative h-8 w-8 rounded-full'>
          <UserAvatarProfile
            user={{
              fullName: 'Local User',
              emailAddresses: [{ emailAddress: 'local@quality-hub.dev' }],
              imageUrl: ''
            }}
          />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent
        className='w-56'
        align='end'
        sideOffset={10}
        forceMount
      >
        <DropdownMenuLabel className='font-normal'>
          <div className='flex flex-col space-y-1'>
            <p className='text-sm leading-none font-medium'>Local User</p>
            <p className='text-muted-foreground text-xs leading-none'>
              local@quality-hub.dev
            </p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem
            onClick={() => router.push('/dashboard/quality-hub/portfolio')}
          >
            Portfolio
          </DropdownMenuItem>
          <DropdownMenuItem
            onClick={() => router.push('/dashboard/quality-hub/pipelines')}
          >
            Pipelines
          </DropdownMenuItem>
          <DropdownMenuItem
            onClick={() =>
              router.push('/dashboard/quality-hub/workspace/teams')
            }
          >
            Teams
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          onClick={async () => {
            await disconnectGitlabToken();
            router.push('/auth/token');
          }}
        >
          Disconnect Token
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
