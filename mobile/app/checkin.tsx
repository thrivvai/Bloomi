import * as Haptics from 'expo-haptics';
import { router } from 'expo-router';
import { useState } from 'react';
import {
  ActivityIndicator,
  Alert,
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
import { useCreateCheckin } from '@/hooks/useCheckin';
import type { CheckinType } from '@/types/api';

const MOOD_CHIPS = [
  { label: 'Struggling', score: 2 },
  { label: 'Low', score: 4 },
  { label: 'Okay', score: 6 },
  { label: 'Good', score: 7 },
  { label: 'Great', score: 9 },
];

function getCheckinType(): CheckinType {
  const h = new Date().getHours();
  if (h < 11) return 'morning';
  if (h < 17) return 'day';
  return 'evening';
}

export default function CheckinModal() {
  const checkinType = getCheckinType();
  const [moodScore, setMoodScore] = useState<number | null>(null);
  const [intention, setIntention] = useState('');
  const createCheckin = useCreateCheckin();

  async function handleSave() {
    if (!moodScore) return;
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    try {
      const result = await createCheckin.mutateAsync({
        checkin_type: checkinType,
        mood_score: moodScore,
        intention_text: intention.trim() || undefined,
      });
      Alert.alert('Check-in saved', result.companion_reaction, [
        { text: 'Thanks', onPress: () => router.back() },
      ]);
    } catch {
      Alert.alert('Could not save check-in', 'Please try again.');
    }
  }

  const TITLES: Record<CheckinType, string> = {
    morning: 'Good morning 🌤',
    day: 'Checking in 🌿',
    evening: 'Winding down 🌙',
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
        <TouchableOpacity style={styles.dismiss} onPress={() => router.back()}>
          <Text style={styles.dismissText}>✕</Text>
        </TouchableOpacity>

        <Text style={styles.title}>{TITLES[checkinType]}</Text>
        <Text style={styles.sub}>How are you feeling right now?</Text>

        <View style={styles.moodRow}>
          {MOOD_CHIPS.map((c) => (
            <TouchableOpacity
              key={c.score}
              style={[styles.moodChip, moodScore === c.score && styles.moodChipSelected]}
              onPress={() => setMoodScore(c.score)}
            >
              <Text style={[styles.moodLabel, moodScore === c.score && styles.moodLabelSelected]}>
                {c.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.intentionLabel}>Set an intention (optional)</Text>
        <TextInput
          style={styles.intentionInput}
          value={intention}
          onChangeText={setIntention}
          placeholder="Today I want to…"
          placeholderTextColor={Colors.textMuted}
          maxLength={256}
          returnKeyType="done"
        />

        <TouchableOpacity
          style={[styles.saveBtn, (!moodScore || createCheckin.isPending) && styles.saveBtnDisabled]}
          onPress={handleSave}
          disabled={!moodScore || createCheckin.isPending}
        >
          {createCheckin.isPending ? (
            <ActivityIndicator color={Colors.white} />
          ) : (
            <Text style={styles.saveBtnText}>Save check-in</Text>
          )}
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.skyCream },
  scroll: { paddingHorizontal: Spacing.lg, paddingBottom: Spacing['2xl'], gap: Spacing.lg, paddingTop: Spacing.md },
  dismiss: { alignSelf: 'flex-end', padding: Spacing.sm },
  dismissText: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.lg, color: Colors.textMuted },
  title: { fontFamily: Typography.fontHeading, fontSize: Typography.size['2xl'], color: Colors.textPrimary },
  sub: { fontFamily: Typography.fontBody, fontSize: Typography.size.base, color: Colors.textSecondary },
  moodRow: { flexDirection: 'row', flexWrap: 'wrap', gap: Spacing.sm },
  moodChip: {
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: Radius.full,
    backgroundColor: Colors.white,
    borderWidth: 1.5,
    borderColor: Colors.border,
  },
  moodChipSelected: { backgroundColor: Colors.deepMoss, borderColor: Colors.deepMoss },
  moodLabel: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.textSecondary },
  moodLabelSelected: { color: Colors.white },
  intentionLabel: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.textMuted, textTransform: 'uppercase', letterSpacing: 0.6 },
  intentionInput: {
    backgroundColor: Colors.white,
    borderRadius: Radius.lg,
    borderWidth: 1.5,
    borderColor: Colors.border,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm + 4,
    fontFamily: Typography.fontBody,
    fontSize: Typography.size.base,
    color: Colors.textPrimary,
  },
  saveBtn: { backgroundColor: Colors.leafGreen, borderRadius: Radius.lg, paddingVertical: Spacing.md, alignItems: 'center' },
  saveBtnDisabled: { opacity: 0.4 },
  saveBtnText: { fontFamily: Typography.fontHeadingSemi, fontSize: Typography.size.md, color: Colors.white },
});
