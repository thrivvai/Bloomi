import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors } from '@/constants/colors';
import { Spacing, Typography, Radius } from '@/constants/theme';
import type { CompanionKind } from '@/types/api';
import { useOnboardingStore } from '@/store/onboardingStore';

const OPTIONS: Array<{
  kind: CompanionKind;
  label: string;
  tagline: string;
  defaultSpecies: string;
  accentColor: string;
}> = [
  {
    kind: 'pet',
    label: 'A pet companion',
    tagline: 'Warm, expressive, and always excited to see you',
    defaultSpecies: 'fluffy_bean',
    accentColor: Colors.bloomCoral,
  },
  {
    kind: 'plant',
    label: 'A plant companion',
    tagline: 'Calm, growing, and beautifully alive with care',
    defaultSpecies: 'monstera',
    accentColor: Colors.leafGreen,
  },
];

export default function ChooseScreen() {
  const { setCompanionKind, setSpeciesCode } = useOnboardingStore();

  function handleSelect(kind: CompanionKind, speciesCode: string) {
    setCompanionKind(kind);
    setSpeciesCode(speciesCode);
    router.push('/onboarding/name');
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.eyebrow}>Welcome to Bloomi</Text>
        <Text style={styles.title}>Who will grow{'\n'}alongside you?</Text>
        <Text style={styles.subtitle}>
          Your choice shapes your experience — both paths lead to real growth.
        </Text>
      </View>

      <View style={styles.options}>
        {OPTIONS.map((opt) => (
          <TouchableOpacity
            key={opt.kind}
            style={[styles.card, { borderColor: opt.accentColor }]}
            onPress={() => handleSelect(opt.kind, opt.defaultSpecies)}
            activeOpacity={0.85}
          >
            <View style={[styles.iconPlaceholder, { backgroundColor: opt.accentColor + '22' }]}>
              <Text style={[styles.iconEmoji]}>{opt.kind === 'pet' ? '🐾' : '🌿'}</Text>
            </View>
            <Text style={styles.cardTitle}>{opt.label}</Text>
            <Text style={styles.cardTagline}>{opt.tagline}</Text>
            <View style={[styles.chooseBadge, { backgroundColor: opt.accentColor }]}>
              <Text style={styles.chooseBadgeText}>Choose</Text>
            </View>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.footer}>You can always change your mind later.</Text>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.skyCream,
    paddingHorizontal: Spacing.lg,
  },
  header: {
    paddingTop: Spacing['2xl'],
    paddingBottom: Spacing.xl,
    gap: Spacing.sm,
  },
  eyebrow: {
    fontFamily: Typography.fontBodyMedium,
    fontSize: Typography.size.sm,
    color: Colors.leafGreen,
    textTransform: 'uppercase',
    letterSpacing: 1.2,
  },
  title: {
    fontFamily: Typography.fontHeading,
    fontSize: Typography.size['2xl'],
    color: Colors.textPrimary,
    lineHeight: Typography.size['2xl'] * 1.2,
  },
  subtitle: {
    fontFamily: Typography.fontBody,
    fontSize: Typography.size.base,
    color: Colors.textSecondary,
    lineHeight: Typography.size.base * 1.6,
  },
  options: {
    flex: 1,
    gap: Spacing.md,
  },
  card: {
    backgroundColor: Colors.white,
    borderRadius: Radius.xl,
    borderWidth: 2,
    padding: Spacing.lg,
    gap: Spacing.sm,
    alignItems: 'flex-start',
  },
  iconPlaceholder: {
    width: 64,
    height: 64,
    borderRadius: Radius.lg,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: Spacing.xs,
  },
  iconEmoji: {
    fontSize: 32,
  },
  cardTitle: {
    fontFamily: Typography.fontHeadingSemi,
    fontSize: Typography.size.lg,
    color: Colors.textPrimary,
  },
  cardTagline: {
    fontFamily: Typography.fontBody,
    fontSize: Typography.size.base,
    color: Colors.textSecondary,
    lineHeight: Typography.size.base * 1.5,
  },
  chooseBadge: {
    marginTop: Spacing.xs,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.xs,
    borderRadius: Radius.full,
  },
  chooseBadgeText: {
    fontFamily: Typography.fontBodyMedium,
    fontSize: Typography.size.sm,
    color: Colors.white,
  },
  footer: {
    fontFamily: Typography.fontBody,
    fontSize: Typography.size.sm,
    color: Colors.textMuted,
    textAlign: 'center',
    paddingVertical: Spacing.lg,
  },
});
