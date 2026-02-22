'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import {
  addTeamMember,
  createTeam,
  listTeamMembers,
  listTeams
} from '@/features/quality-hub/api/client';
import { Team, TeamMember } from '@/features/quality-hub/types';
import { useCallback, useEffect, useState } from 'react';

export function TeamManagement() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeamId, setSelectedTeamId] = useState<number | null>(null);
  const [members, setMembers] = useState<TeamMember[]>([]);
  const [teamName, setTeamName] = useState('');
  const [memberUserId, setMemberUserId] = useState('');
  const [memberRole, setMemberRole] = useState('member');
  const [error, setError] = useState<string | null>(null);

  const loadTeams = useCallback(async () => {
    try {
      const data = await listTeams();
      setTeams(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load teams');
    }
  }, []);

  const loadMembers = useCallback(async (teamId: number) => {
    try {
      const data = await listTeamMembers(teamId);
      setMembers(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to load team members'
      );
    }
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void loadTeams();
  }, [loadTeams]);

  useEffect(() => {
    if (!selectedTeamId && teams.length > 0) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setSelectedTeamId(teams[0].id);
    }
  }, [selectedTeamId, teams]);

  useEffect(() => {
    if (selectedTeamId) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      void loadMembers(selectedTeamId);
    }
  }, [loadMembers, selectedTeamId]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Teams & Memberships</CardTitle>
      </CardHeader>
      <CardContent className='space-y-4'>
        {error && <p className='text-destructive text-sm'>{error}</p>}

        <div className='flex gap-2'>
          <Input
            placeholder='New team name'
            value={teamName}
            onChange={(event) => setTeamName(event.target.value)}
          />
          <Button
            onClick={async () => {
              if (!teamName.trim()) return;
              await createTeam({ name: teamName.trim() });
              setTeamName('');
              await loadTeams();
            }}
          >
            Create Team
          </Button>
        </div>

        <div className='flex flex-wrap gap-2'>
          {teams.map((team) => (
            <Button
              key={team.id}
              variant={selectedTeamId === team.id ? 'default' : 'outline'}
              onClick={() => setSelectedTeamId(team.id)}
            >
              {team.name}
            </Button>
          ))}
        </div>

        {selectedTeamId && (
          <div className='space-y-2 rounded-md border p-3'>
            <h4 className='font-medium'>Members</h4>
            <div className='flex gap-2'>
              <Input
                placeholder='User ID'
                value={memberUserId}
                onChange={(event) => setMemberUserId(event.target.value)}
              />
              <Input
                placeholder='Role (owner/admin/member)'
                value={memberRole}
                onChange={(event) => setMemberRole(event.target.value)}
              />
              <Button
                onClick={async () => {
                  if (!memberUserId.trim()) return;
                  await addTeamMember(selectedTeamId, {
                    user_id: Number(memberUserId),
                    role: memberRole
                  });
                  setMemberUserId('');
                  await loadMembers(selectedTeamId);
                }}
              >
                Add Member
              </Button>
            </div>

            <div className='space-y-1'>
              {members.length === 0 && (
                <p className='text-muted-foreground text-sm'>
                  No members in this team yet.
                </p>
              )}
              {members.map((member) => (
                <p key={member.id} className='text-sm'>
                  Member #{member.id} | user {member.user_id} | role{' '}
                  {member.role}
                </p>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
