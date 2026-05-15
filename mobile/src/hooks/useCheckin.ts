import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/api/client';
import type { Checkin, CheckinType } from '@/types/api';

export function useCreateCheckin() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: {
      checkin_type: CheckinType;
      mood_score?: number;
      mood_label?: string;
      energy_level?: number;
      intention_text?: string;
      gratitude_text?: string;
      stress_score?: number;
    }) => api.post<Checkin>('/v1/checkins', payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['home', 'state'] });
    },
  });
}
