import { router } from 'expo-router';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors } from '@/constants/colors';
import { Radius, Spacing, Typography } from '@/constants/theme';
import type { EmotionalTone } from '@/types/api';
import { useOnboardingStore } from '@/store/onboardingStore';

const TONES: Array<{ tone: EmotionalTone; label: string; description: string; emoji: string }> = [
  { tone: 'calm', label: 'Calm & gentle', description: 'Soft check-ins, spacious pacing', emoji: '🌊' },
  { tone: 'warm', label: 'Warm & supportive', description: 'Encouraging words, cozy energy', emoji: '☀️' },
  { tone: 'grounded', label: 'Grounded & steady', description: 'Clear, honest, no fluff', emoji: '🪨' },
  { tone: 'playful', label: 'Playful & light', description: 'Fun prompts, lighthearted vibe', emoji: '✨' },
];

export default function ArchetypeScreen() {
  const { companionName, emotionalTone, setEmotionalTone } = useOnboardingStore();

  function handleContinue() {
    router.push('/onboarding/goals');
  }

  return (
    <SafeAreaView style={styles.container}>
      <TouchableOpacity style={styles.back} onPress={() => router.back()}>
        <Text style={styles.backText}>← Back</Text>
      </TouchableOpacity>

      <View style={styles.content}>
        <Text style={styles.title}>How should{'\n'}{companionName} support you?</Text>
        <Text style={styles.subtitle}>
          This sets the emotional tone of your experience. You can adjust it anytime.
        </Text>

        <View style={styles.options}>
          {TONES.map((item) => {
            const selected = emotionalTone === item.tone;
            return (
              <TouchableOpacity
                key={item.tone}
                style={[styles.card, selected && styles.cardSelected]}
                onPress={() => setEmotionalTone(item.tone)}
                activeOpacity={0.8}
              >
                <Text style={styles.cardEmoji}>{item.emoji}</Text>
                <View style={{ flex: 1 }}>
                  <Text style={[styles.cardLabel, selected && styles.cardLabelSelected]}>
                    {item.label}
                  </Text>
                  <Text style={styles.cardDesc}>{item.description}</Text>
                </View>
                <View style={[styles.radio, selected && styles.radioSelected]} />
              </TouchableOpacity>
            );
          })}
        </View>
      </View>

      <View style={styles.footer}>
        <TouchableOpacity style={styles.button} onPress={handleContinue}>
          <Text style={styles.buttonText}>{emotionalTone ? 'Continue' : 'Skip for now'}</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.skyCream },
  back: { paddingHorizontal: Spacing.lg, paddingTop: Spacing.md },
  backText: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.base, color: Colors.textSecondary },
  content: { flex: 1, paddingHorizontal: Spacing.lg, paddingTop: Spacing.xl, gap: Spacing.lg },
  title: { fontFamily: Typography.fontHeading, fontSize: Typography.size['2xl'], color: Colors.textPrimary, lineHeight: Typography.size['2xl'] * 1.2 },
  subtitle: { fontFamily: Typography.fontBody, fontSize: Typography.size.base, color: Colors.textSecondary, lineHeight: Typography.size.base * 1.6 },
  options: { gap: Spacing.sm },
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.white,
    borderRadius: Radius.lg,
    padding: Spacing.md,
    gap: Spacing.md,
    borderWidth: 2,
    borderColor: Colors.border,
  },
  cardSelected: { borderColor: Colors.leafGreen, backgroundColor: '#6FAF7B11' },
  cardEmoji: { fontSize: 28, width: 40, textAlign: 'center' },
  cardLabel: { fontFamily: Typography.fontHeadingSemi, fontSize: Typography.size.base, color: Colors.textPrimary },
  cardLabelSelected: { color: Colors.deepMoss },
  cardDesc: { fontFamily: Typography.fontBody, fontSize: Typography.size.sm, color: Colors.textSecondary, marginTop: 2 },
  radio: { width: 20, height: 20, borderRadius: 10, borderWidth: 2, borderColor: Colors.border },
  radioSelected: { borderColor: Colors.leafGreen, backgroundColor: Colors.leafGreen },
  footer: { padding: Spacing.lg },
  button: { backgroundColor: Colors.leafGreen, borderRadius: Radius.lg, paddingVertical: Spacing.md, alignItems: 'center' },
  buttonText: { fontFamily: Typography.fontHeadingSemi, fontSize: Typography.size.md, color: Colors.white },
});
