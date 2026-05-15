import * as Haptics from 'expo-haptics';
import { useState } from 'react';
import { ActivityIndicator, Alert, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors } from '@/constants/colors';
import { Radius, Shadow, Spacing, Typography } from '@/constants/theme';
import { useGoals, useCompleteGoal } from '@/hooks/useGoals';
import type { Goal } from '@/types/api';

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: Colors.leafGreen,
  medium: Colors.bloomCoral,
  hard: Colors.softClay,
};

function GoalCard({ goal }: { goal: Goal }) {
  const completeGoal = useCompleteGoal();

  async function handleComplete() {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    try {
      const result = await completeGoal.mutateAsync({ goalId: goal.id, payload: {} });
      Alert.alert(
        result.level_up ? '🎉 Level up!' : '✨ Nice work!',
        `+${result.energy_awarded} energy  +${result.coins_awarded} coins\n${result.companion_reaction === 'level_up' ? 'Your Bloomi leveled up!' : 'Your Bloomi feels the care.'}`,
      );
    } catch {}
  }

  return (
    <View style={styles.goalCard}>
      <View style={styles.goalLeft}>
        <View style={[styles.diffDot, { backgroundColor: DIFFICULTY_COLORS[goal.difficulty_tier] ?? Colors.leafGreen }]} />
        <View style={{ flex: 1 }}>
          <Text style={styles.goalTitle}>{goal.title}</Text>
          <Text style={styles.goalMeta}>
            {goal.cadence ?? 'once'}{goal.category ? ` · ${goal.category}` : ''}
          </Text>
        </View>
      </View>
      <TouchableOpacity
        style={[styles.doneBtn, completeGoal.isPending && styles.doneBtnLoading]}
        onPress={handleComplete}
        disabled={completeGoal.isPending}
      >
        <Text style={styles.doneBtnText}>{completeGoal.isPending ? '…' : 'Done'}</Text>
      </TouchableOpacity>
    </View>
  );
}

export default function GoalsScreen() {
  const { data: goals, isLoading } = useGoals();

  if (isLoading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color={Colors.leafGreen} size="large" />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll} showsVerticalScrollIndicator={false}>
        <Text style={styles.screenTitle}>Your goals</Text>
        <Text style={styles.screenSub}>A tiny step still counts.</Text>

        {(!goals || goals.length === 0) && (
          <View style={styles.emptyState}>
            <Text style={styles.emptyEmoji}>🌱</Text>
            <Text style={styles.emptyText}>No goals yet. Add one to get started.</Text>
          </View>
        )}

        {goals?.map((g) => <GoalCard key={g.id} goal={g} />)}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.skyCream },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: Colors.skyCream },
  scroll: { paddingHorizontal: Spacing.lg, paddingBottom: Spacing['3xl'], gap: Spacing.md, paddingTop: Spacing.lg },
  screenTitle: { fontFamily: Typography.fontHeading, fontSize: Typography.size.xl, color: Colors.textPrimary },
  screenSub: { fontFamily: Typography.fontBody, fontSize: Typography.size.base, color: Colors.textSecondary },
  goalCard: {
    backgroundColor: Colors.white,
    borderRadius: Radius.lg,
    padding: Spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: Spacing.md,
    ...Shadow.soft,
  },
  goalLeft: { flex: 1, flexDirection: 'row', alignItems: 'center', gap: Spacing.sm },
  diffDot: { width: 10, height: 10, borderRadius: 5 },
  goalTitle: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.base, color: Colors.textPrimary },
  goalMeta: { fontFamily: Typography.fontBody, fontSize: Typography.size.sm, color: Colors.textMuted, marginTop: 2 },
  doneBtn: { backgroundColor: Colors.leafGreen, borderRadius: Radius.full, paddingHorizontal: Spacing.md, paddingVertical: Spacing.xs + 2 },
  doneBtnLoading: { opacity: 0.5 },
  doneBtnText: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.white },
  emptyState: { alignItems: 'center', paddingVertical: Spacing['2xl'], gap: Spacing.sm },
  emptyEmoji: { fontSize: 48 },
  emptyText: { fontFamily: Typography.fontBody, fontSize: Typography.size.base, color: Colors.textMuted, textAlign: 'center' },
});
