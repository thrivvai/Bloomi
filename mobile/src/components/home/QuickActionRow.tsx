import * as Haptics from 'expo-haptics';
import { router } from 'expo-router';
import { ScrollView, StyleSheet, Text, TouchableOpacity } from 'react-native';
import { Colors } from '@/constants/colors';
import { Radius, Shadow, Spacing, Typography } from '@/constants/theme';
import type { QuickAction } from '@/types/api';

const ACTION_EMOJI: Record<string, string> = {
  checkin: '✏️',
  breathwork: '💨',
  goal: '✅',
  journal: '📓',
};

interface Props {
  actions: QuickAction[];
}

export function QuickActionRow({ actions }: Props) {
  function handleAction(action: QuickAction) {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    if (action.action_type === 'checkin') {
      router.push('/checkin');
    } else if (action.action_type === 'journal') {
      router.push('/tabs/journal');
    }
  }

  if (!actions.length) return null;

  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={styles.row}
    >
      {actions.map((a, i) => (
        <TouchableOpacity
          key={i}
          style={styles.chip}
          onPress={() => handleAction(a)}
          activeOpacity={0.8}
        >
          <Text style={styles.chipEmoji}>{ACTION_EMOJI[a.action_type] ?? '⚡'}</Text>
          <Text style={styles.chipLabel}>{a.title}</Text>
          {a.duration_seconds && (
            <Text style={styles.chipDuration}>{Math.round(a.duration_seconds / 60)}m</Text>
          )}
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  row: { gap: Spacing.sm, paddingRight: Spacing.lg },
  chip: {
    backgroundColor: Colors.white,
    borderRadius: Radius.xl,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm + 2,
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.xs,
    ...Shadow.soft,
  },
  chipEmoji: { fontSize: 18 },
  chipLabel: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.textPrimary },
  chipDuration: { fontFamily: Typography.fontBody, fontSize: Typography.size.xs, color: Colors.textMuted, marginLeft: 2 },
});
