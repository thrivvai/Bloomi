import * as SecureStore from 'expo-secure-store';
import { create } from 'zustand';

interface AuthState {
  userId: string | null;
  isOnboarded: boolean;
  setUserId: (id: string) => Promise<void>;
  setOnboarded: (value: boolean) => void;
  loadFromStorage: () => Promise<void>;
  clear: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  userId: null,
  isOnboarded: false,

  setUserId: async (id) => {
    await SecureStore.setItemAsync('bloomi_user_id', id);
    set({ userId: id });
  },

  setOnboarded: (value) => {
    set({ isOnboarded: value });
  },

  loadFromStorage: async () => {
    const userId = await SecureStore.getItemAsync('bloomi_user_id');
    const onboarded = await SecureStore.getItemAsync('bloomi_onboarded');
    set({ userId, isOnboarded: onboarded === 'true' });
  },

  clear: async () => {
    await SecureStore.deleteItemAsync('bloomi_user_id');
    await SecureStore.deleteItemAsync('bloomi_onboarded');
    set({ userId: null, isOnboarded: false });
  },
}));
