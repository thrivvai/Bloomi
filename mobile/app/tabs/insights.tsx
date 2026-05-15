import { ActivityIndicator, ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors } from '@/constants/colors';
import { Radius, Shadow, Spacing, Typography } from '@/constants/theme';
import { useWeeklySummary } from '@/hooks/useJournal';

export default function InsightsScreen() {
  const { data, isLoading } = useWeeklySummary();

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
        <Text style={styles.screenTitle}>Weekly recap</Text>
        <Text style={styles.screenSub}>
          {data?.week_start} — {data?.week_end}
        </Text>

        {/* Companion retelling */}
        <View style={styles.retellingCard}>
          <Text style={styles.retellingLabel}>Your Bloomi says</Text>
          <Text style={styles.retellingText}>
            {data?.companion_retelling ?? 'Your Bloomi held space for you this week.'}
          </Text>
        </View>

        {/* Mood */}
        {data?.mood_average != null && (
          <View style={styles.statCard}>
            <Text style={styles.statLabel}>Average mood</Text>
            <Text style={styles.statValue}>{data.mood_average.toFixed(1)} / 10</Text>
            {data.mood_trend && <Text style={styles.statSub}>{data.mood_trend}</Text>}
          </View>
        )}

        {/* Completions */}
        <View style={styles.statCard}>
          <Text style={styles.statLabel}>Goals completed</Text>
          <Text style={styles.statValue}>{data?.completions_count ?? 0}</Text>
        </View>

        {/* Top wins */}
        {data?.top_wins && data.top_wins.length > 0 && (
          <View style={styles.listCard}>
            <Text style={styles.listTitle}>Top wins</Text>
            {data.top_wins.map((win, i) => (
              <Text key={i} style={styles.listItem}>✦ {win}</Text>
            ))}
          </View>
        )}

        {/* Reset suggestion */}
        {data?.reset_suggestion && (
          <View style={styles.resetCard}>
            <Text style={styles.resetText}>{data.reset_suggestion}</Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.skyCream },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: Colors.skyCream },
  scroll: { paddingHorizontal: Spacing.lg, paddingBottom: Spacing['3xl'], gap: Spacing.md, paddingTop: Spacing.lg },
  screenTitle: { fontFamily: Typography.fontHeading, fontSize: Typography.size.xl, color: Colors.textPrimary },
  screenSub: { fontFamily: Typography.fontBody, fontSize: Typography.size.sm, color: Colors.textMuted },
  retellingCard: {
    backgroundColor: Colors.deepMoss,
    borderRadius: Radius.xl,
    padding: Spacing.lg,
    gap: Spacing.sm,
    ...Shadow.card,
  },
  retellingLabel: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.xs, color: Colors.leafGreen, textTransform: 'uppercase', letterSpacing: 0.8 },
  retellingText: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.md, color: Colors.white, lineHeight: Typography.size.md * 1.6 },
  statCard: {
    backgroundColor: Colors.white,
    borderRadius: Radius.lg,
    padding: Spacing.lg,
    ...Shadow.soft,
  },
  statLabel: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.textMuted, textTransform: 'uppercase', letterSpacing: 0.6 },
  statValue: { fontFamily: Typography.fontHeading, fontSize: Typography.size['2xl'], color: Colors.textPrimary, marginTop: 4 },
  statSub: { fontFamily: Typography.fontBody, fontSize: Typography.size.sm, color: Colors.textSecondary, marginTop: 4 },
  listCard: { backgroundColor: Colors.white, borderRadius: Radius.lg, padding: Spacing.lg, gap: Spacing.sm, ...Shadow.soft },
  listTitle: { fontFamily: Typography.fontHeadingSemi, fontSize: Typography.size.base, color: Colors.textPrimary },
  listItem: { fontFamily: Typography.fontBody, fontSize: Typography.size.base, color: Colors.textSecondary, lineHeight: Typography.size.base * 1.6 },
  resetCard: { backgroundColor: Colors.surfaceSubtle, borderRadius: Radius.lg, padding: Spacing.lg, borderLeftWidth: 3, borderLeftColor: Colors.bloomCoral },
  resetText: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.base, color: Colors.textSecondary, lineHeight: Typography.size.base * 1.6 },
});
