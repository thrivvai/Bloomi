import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/api/client';
import type { JournalEntry, WeeklySummary } from '@/types/api';

export function useCreateJournalEntry() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: {
      body_text: string;
      entry_type?: string;
      prompt_id?: string;
      tags?: string[];
      mood_after?: number;
    }) => api.post<JournalEntry>('/v1/journal-entries', payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['insights', 'weekly'] }),
  });
}

export function useWeeklySummary() {
  return useQuery({
    queryKey: ['insights', 'weekly'],
    queryFn: () => api.get<WeeklySummary>('/v1/insights/weekly-summary'),
    staleTime: 5 * 60_000,
  });
}
