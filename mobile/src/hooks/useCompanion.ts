import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/api/client';
import type { CompanionChatResponse, CompanionState } from '@/types/api';

export function useCompanionState() {
  return useQuery({
    queryKey: ['companion', 'state'],
    queryFn: () => api.get<CompanionState>('/v1/companion/state'),
    staleTime: 60_000,
  });
}

export function useCompanionChat() {
  return useMutation({
    mutationFn: (message: string) =>
      api.post<CompanionChatResponse>('/v1/companion/chat', { message }),
  });
}
