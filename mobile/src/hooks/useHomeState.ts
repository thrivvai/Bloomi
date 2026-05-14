import { useQuery } from '@tanstack/react-query';
import { api } from '@/api/client';
import type { HomeState } from '@/types/api';

export function useHomeState() {
  return useQuery({
    queryKey: ['home', 'state'],
    queryFn: () => api.get<HomeState>('/v1/home/state'),
    staleTime: 30_000,
  });
}
