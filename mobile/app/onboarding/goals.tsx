import * as SecureStore from 'expo-secure-store';
import { router } from 'expo-router';
import { useState } from 'react';
import {
  ActivityIndicator,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors } from '@/constants/colors';
import { Radius, Spacing, Typography } from '@/constants/theme';
import { useOnboardingStore } from '@/store/onboardingStore';
import { useAuthStore } from '@/store/authStore';
import { api } from '@/api/client';
import type { OnboardingResult } from '@/types/api';

const SEED_GOALS = [
  { title: 'Drink enough water', cadence: 'daily' },
  { title: 'Step outside for 5 minutes', cadence: 'daily' },
  { title: 'Write one thing I\'m grateful for', cadence: 'daily' },
  { title: 'Move my body', cadence: 'daily' },
  { title: 'Wind down without screens', cadence: 'daily' },
];

export default function GoalsScreen() {
  const store = useOnboardingStore();
  const { setUserId, setOnboarded } = useAuthStore();
  const [customGoal, setCustomGoal] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function toggleSeed(goal: { title: string; cadence: string }) {
    const exists = store.starterGoals.find((g) => g.title === goal.title);
    if (exists) {
      const idx = store.starterGoals.indexOf(exists);
      store.removeStarterGoal(idx);
    } else {
      store.addStarterGoal(goal);
    }
  }

  function addCustom() {
    const t = customGoal.trim();
    if (!t) return;
    store.addStarterGoal({ title: t, cadence: 'daily' });
    setCustomGoal('');
  }

  async function handleFinish() {
    setLoading(true);
    setError(null);
    try {
      // In production this userId comes from Supabase Auth.
      // For now we generate a UUID client-side as a stub.
      const userId = crypto.randomUUID();
      await SecureStore.setItemAsync('bloomi_user_id', userId);

      const result = await api.post<OnboardingResult>('/v1/onboarding/complete', {
        companion_kind: store.companionKind,
        companion_name: store.companionName,
        species_code: store.speciesCode,
        archetype: store.archetype ?? undefined,
        emotional_tone_pref: store.emotionalTone ?? undefined,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        starter_goals: store.starterGoals,
        notifications_enabled: true,
      });

      await setUserId(result.user_id);
      await SecureStore.setItemAsync('bloomi_onboarded', 'true');
      setOnboarded(true);
      store.reset();
      router.replace('/tabs');
    } catch (e: any) {
      setError(e.message ?? 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
        <TouchableOpacity style={styles.back} onPress={() => router.back()}>
          <Text style={styles.backText}>← Back</Text>
        </TouchableOpacity>

        <Text style={styles.title}>Pick a few tiny{'\n'}things to start with</Text>
        <Text style={styles.subtitle}>
          Small wins count. You can add, remove, or change these anytime.
        </Text>

        <View style={styles.seeds}>
          {SEED_GOALS.map((g) => {
            const selected = !!store.starterGoals.find((s) => s.title === g.title);
            return (
              <TouchableOpacity
                key={g.title}
                style={[styles.seedChip, selected && styles.seedChipSelected]}
                onPress={() => toggleSeed(g)}
              >
                <Text style={[styles.seedText, selected && styles.seedTextSelected]}>
                  {selected ? '✓ ' : ''}{g.title}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>

        <View style={styles.customRow}>
          <TextInput
            style={styles.customInput}
            value={customGoal}
            onChangeText={setCustomGoal}
            placeholder="Add your own…"
            placeholderTextColor={Colors.textMuted}
            returnKeyType="done"
            onSubmitEditing={addCustom}
          />
          <TouchableOpacity style={styles.addBtn} onPress={addCustom}>
            <Text style={styles.addBtnText}>+</Text>
          </TouchableOpacity>
        </View>

        {error && <Text style={styles.error}>{error}</Text>}
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleFinish}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color={Colors.white} />
          ) : (
            <Text style={styles.buttonText}>
              {store.starterGoals.length > 0 ? 'Start blooming →' : 'Skip and start →'}
            </Text>
          )}
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.skyCream },
  scroll: { padding: Spacing.lg, gap: Spacing.lg, paddingBottom: 120 },
  back: { marginBottom: Spacing.sm },
  backText: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.base, color: Colors.textSecondary },
  title: { fontFamily: Typography.fontHeading, fontSize: Typography.size['2xl'], color: Colors.textPrimary, lineHeight: Typography.size['2xl'] * 1.2 },
  subtitle: { fontFamily: Typography.fontBody, fontSize: Typography.size.base, color: Colors.textSecondary, lineHeight: Typography.size.base * 1.6 },
  seeds: { flexDirection: 'row', flexWrap: 'wrap', gap: Spacing.sm },
  seedChip: {
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: Radius.full,
    backgroundColor: Colors.white,
    borderWidth: 1.5,
    borderColor: Colors.border,
  },
  seedChipSelected: { backgroundColor: Colors.deepMoss, borderColor: Colors.deepMoss },
  seedText: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.textSecondary },
  seedTextSelected: { color: Colors.white },
  customRow: { flexDirection: 'row', gap: Spacing.sm },
  customInput: {
    flex: 1,
    backgroundColor: Colors.white,
    borderRadius: Radius.lg,
    borderWidth: 1.5,
    borderColor: Colors.border,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm + 2,
    fontFamily: Typography.fontBody,
    fontSize: Typography.size.base,
    color: Colors.textPrimary,
  },
  addBtn: {
    backgroundColor: Colors.leafGreen,
    borderRadius: Radius.lg,
    width: 48,
    alignItems: 'center',
    justifyContent: 'center',
  },
  addBtnText: { color: Colors.white, fontSize: 24, fontFamily: Typography.fontHeading, lineHeight: 28 },
  error: { fontFamily: Typography.fontBody, fontSize: Typography.size.sm, color: Colors.error, textAlign: 'center' },
  footer: { padding: Spacing.lg, paddingBottom: Spacing.xl },
  button: { backgroundColor: Colors.leafGreen, borderRadius: Radius.lg, paddingVertical: Spacing.md + 2, alignItems: 'center' },
  buttonDisabled: { opacity: 0.6 },
  buttonText: { fontFamily: Typography.fontHeadingSemi, fontSize: Typography.size.md, color: Colors.white },
});
