import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/api/client';
import type { Goal, GoalCompletion } from '@/types/api';

export function useGoals() {
  return useQuery({
    queryKey: ['goals'],
    queryFn: () => api.get<Goal[]>('/v1/goals'),
  });
}

export function useCreateGoal() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: {
      title: string;
      goal_type?: string;
      cadence?: string;
      difficulty_tier?: string;
      duration_minutes?: number;
      category?: string;
      proof_requirement?: string;
    }) => api.post<Goal>('/v1/goals', payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['goals'] }),
  });
}

export function useCompleteGoal() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      goalId,
      payload,
    }: {
      goalId: string;
      payload: { mood_before?: number; mood_after?: number };
    }) => api.post<GoalCompletion>(`/v1/goals/${goalId}/complete`, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['goals'] });
      qc.invalidateQueries({ queryKey: ['home', 'state'] });
      qc.invalidateQueries({ queryKey: ['companion', 'state'] });
    },
  });
}
