import * as Haptics from 'expo-haptics';
import { router } from 'expo-router';
import { ActivityIndicator, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors } from '@/constants/colors';
import { Radius, Shadow, Spacing, Typography } from '@/constants/theme';
import { useHomeState } from '@/hooks/useHomeState';
import { CompanionView } from '@/components/companion/CompanionView';
import { QuickActionRow } from '@/components/home/QuickActionRow';
import { WalletBadges } from '@/components/home/WalletBadges';

export default function HomeScreen() {
  const { data, isLoading, isError, refetch } = useHomeState();

  if (isLoading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color={Colors.leafGreen} size="large" />
      </View>
    );
  }

  if (isError || !data) {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorText}>Something gentle went wrong.</Text>
        <TouchableOpacity onPress={() => refetch()} style={styles.retryBtn}>
          <Text style={styles.retryText}>Try again</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scroll}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.headerRow}>
          <Text style={styles.greeting}>{data.contextual_greeting}</Text>
          <WalletBadges balances={data.wallet_balances} />
        </View>

        {/* Companion */}
        <CompanionView companion={data.companion} />

        {/* Companion name + stage */}
        <View style={styles.companionMeta}>
          <Text style={styles.companionName}>{data.companion.name}</Text>
          <Text style={styles.companionStage}>
            Level {data.companion.level} · {data.companion.stage}
          </Text>
        </View>

        {/* Suggested action */}
        {data.suggested_next_action && (
          <TouchableOpacity
            style={styles.suggestedCard}
            onPress={() => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              if (data.suggested_next_action?.action_type === 'checkin') {
                router.push('/checkin');
              }
            }}
            activeOpacity={0.85}
          >
            <View>
              <Text style={styles.suggestedLabel}>Suggested</Text>
              <Text style={styles.suggestedTitle}>{data.suggested_next_action.title}</Text>
            </View>
            <Text style={styles.suggestedArrow}>→</Text>
          </TouchableOpacity>
        )}

        {/* Quick actions */}
        <QuickActionRow actions={data.quick_actions} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.skyCream },
  scroll: { paddingHorizontal: Spacing.lg, paddingBottom: Spacing['3xl'], gap: Spacing.md },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: Colors.skyCream, gap: Spacing.md },
  headerRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingTop: Spacing.md },
  greeting: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.base, color: Colors.textSecondary, flex: 1 },
  companionMeta: { alignItems: 'center', gap: 4 },
  companionName: { fontFamily: Typography.fontHeading, fontSize: Typography.size.xl, color: Colors.textPrimary },
  companionStage: { fontFamily: Typography.fontBody, fontSize: Typography.size.sm, color: Colors.textMuted },
  suggestedCard: {
    backgroundColor: Colors.deepMoss,
    borderRadius: Radius.xl,
    padding: Spacing.lg,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    ...Shadow.card,
  },
  suggestedLabel: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.xs, color: Colors.leafGreen, textTransform: 'uppercase', letterSpacing: 0.8 },
  suggestedTitle: { fontFamily: Typography.fontHeadingSemi, fontSize: Typography.size.md, color: Colors.white, marginTop: 4 },
  suggestedArrow: { fontSize: Typography.size.xl, color: Colors.leafGreen },
  errorText: { fontFamily: Typography.fontBody, fontSize: Typography.size.base, color: Colors.textSecondary },
  retryBtn: { paddingHorizontal: Spacing.lg, paddingVertical: Spacing.sm, backgroundColor: Colors.leafGreen, borderRadius: Radius.full },
  retryText: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.white },
});
