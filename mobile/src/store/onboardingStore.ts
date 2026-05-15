import { create } from 'zustand';
import type { CompanionKind, EmotionalTone } from '@/types/api';

interface StarterGoal {
  title: string;
  cadence: string;
}

interface OnboardingState {
  companionKind: CompanionKind | null;
  companionName: string;
  speciesCode: string;
  archetype: string | null;
  emotionalTone: EmotionalTone | null;
  starterGoals: StarterGoal[];

  setCompanionKind: (kind: CompanionKind) => void;
  setCompanionName: (name: string) => void;
  setSpeciesCode: (code: string) => void;
  setArchetype: (archetype: string) => void;
  setEmotionalTone: (tone: EmotionalTone) => void;
  addStarterGoal: (goal: StarterGoal) => void;
  removeStarterGoal: (index: number) => void;
  reset: () => void;
}

const initial = {
  companionKind: null,
  companionName: '',
  speciesCode: '',
  archetype: null,
  emotionalTone: null,
  starterGoals: [],
};

export const useOnboardingStore = create<OnboardingState>((set) => ({
  ...initial,

  setCompanionKind: (kind) => set({ companionKind: kind }),
  setCompanionName: (name) => set({ companionName: name }),
  setSpeciesCode: (code) => set({ speciesCode: code }),
  setArchetype: (archetype) => set({ archetype }),
  setEmotionalTone: (tone) => set({ emotionalTone: tone }),

  addStarterGoal: (goal) =>
    set((s) => ({ starterGoals: [...s.starterGoals, goal] })),

  removeStarterGoal: (index) =>
    set((s) => ({ starterGoals: s.starterGoals.filter((_, i) => i !== index) })),

  reset: () => set(initial),
}));
