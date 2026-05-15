import { StyleSheet, Text, View } from 'react-native';
import { Colors } from '@/constants/colors';
import { Radius, Spacing, Typography } from '@/constants/theme';
import type { CompanionState } from '@/types/api';

const STAGE_EMOJI: Record<string, string> = {
  seedling: '🌱',
  sprout: '🌿',
  bloom: '🌸',
  flourishing: '🌳',
};

const MOOD_EMOJI: Record<string, string> = {
  content: '😊',
  happy: '😄',
  tired: '😴',
  excited: '🤩',
  calm: '😌',
};

interface Props {
  companion: CompanionState;
}

export function CompanionView({ companion }: Props) {
  const stageEmoji = STAGE_EMOJI[companion.stage] ?? '🌱';
  const moodEmoji = MOOD_EMOJI[companion.mood_state] ?? '😊';
  const xpPercent = Math.min(100, companion.xp);

  return (
    <View style={styles.container}>
      {/* Companion avatar placeholder — swap with Rive/Lottie in Phase 3 */}
      <View style={styles.avatarRing}>
        <Text style={styles.companionEmoji}>{stageEmoji}</Text>
        <Text style={styles.moodBadge}>{moodEmoji}</Text>
      </View>

      {/* XP bar */}
      <View style={styles.xpBarTrack}>
        <View style={[styles.xpBarFill, { width: `${xpPercent}%` }]} />
      </View>
      <Text style={styles.xpLabel}>
        Level {companion.level} · {companion.xp} / 100 XP
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    paddingVertical: Spacing.xl,
    gap: Spacing.md,
  },
  avatarRing: {
    width: 160,
    height: 160,
    borderRadius: 80,
    backgroundColor: Colors.surfaceSubtle,
    borderWidth: 4,
    borderColor: Colors.leafGreen + '44',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },
  companionEmoji: {
    fontSize: 80,
    lineHeight: 96,
  },
  moodBadge: {
    position: 'absolute',
    bottom: 8,
    right: 8,
    fontSize: 28,
    backgroundColor: Colors.white,
    borderRadius: 20,
    padding: 4,
    overflow: 'hidden',
  },
  xpBarTrack: {
    width: '60%',
    height: 6,
    backgroundColor: Colors.border,
    borderRadius: Radius.full,
    overflow: 'hidden',
  },
  xpBarFill: {
    height: '100%',
    backgroundColor: Colors.leafGreen,
    borderRadius: Radius.full,
  },
  xpLabel: {
    fontFamily: Typography.fontBody,
    fontSize: Typography.size.xs,
    color: Colors.textMuted,
  },
});
