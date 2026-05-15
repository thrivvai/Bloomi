import { router } from 'expo-router';
import { useState } from 'react';
import {
  KeyboardAvoidingView,
  Platform,
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

const SUGGESTIONS_BY_KIND: Record<string, string[]> = {
  pet: ['Pip', 'Mochi', 'Bean', 'Fern', 'Clover'],
  plant: ['Moss', 'Sage', 'Ivy', 'Wren', 'Cedar'],
};

export default function NameScreen() {
  const { companionKind, setCompanionName } = useOnboardingStore();
  const [name, setName] = useState('');

  const suggestions = SUGGESTIONS_BY_KIND[companionKind ?? 'pet'] ?? [];

  function handleContinue() {
    if (!name.trim()) return;
    setCompanionName(name.trim());
    router.push('/onboarding/archetype');
  }

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <TouchableOpacity style={styles.back} onPress={() => router.back()}>
          <Text style={styles.backText}>← Back</Text>
        </TouchableOpacity>

        <View style={styles.content}>
          <Text style={styles.title}>Give your{'\n'}Bloomi a name</Text>
          <Text style={styles.subtitle}>
            This is the name you'll see every day. Make it yours.
          </Text>

          <TextInput
            style={styles.input}
            value={name}
            onChangeText={setName}
            placeholder="e.g. Sage, Pip, Fern…"
            placeholderTextColor={Colors.textMuted}
            maxLength={24}
            autoFocus
            autoCapitalize="words"
            returnKeyType="done"
            onSubmitEditing={handleContinue}
          />

          <Text style={styles.suggestLabel}>Quick picks</Text>
          <View style={styles.suggestions}>
            {suggestions.map((s) => (
              <TouchableOpacity
                key={s}
                style={[styles.chip, name === s && styles.chipActive]}
                onPress={() => setName(s)}
              >
                <Text style={[styles.chipText, name === s && styles.chipTextActive]}>{s}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <View style={styles.footer}>
          <TouchableOpacity
            style={[styles.button, !name.trim() && styles.buttonDisabled]}
            onPress={handleContinue}
            disabled={!name.trim()}
          >
            <Text style={styles.buttonText}>Continue</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.skyCream },
  back: { paddingHorizontal: Spacing.lg, paddingTop: Spacing.md },
  backText: {
    fontFamily: Typography.fontBodyMedium,
    fontSize: Typography.size.base,
    color: Colors.textSecondary,
  },
  content: {
    flex: 1,
    paddingHorizontal: Spacing.lg,
    paddingTop: Spacing.xl,
    gap: Spacing.md,
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
  input: {
    backgroundColor: Colors.white,
    borderRadius: Radius.lg,
    borderWidth: 2,
    borderColor: Colors.border,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.md,
    fontFamily: Typography.fontHeadingSemi,
    fontSize: Typography.size.xl,
    color: Colors.textPrimary,
    marginTop: Spacing.md,
  },
  suggestLabel: {
    fontFamily: Typography.fontBodyMedium,
    fontSize: Typography.size.sm,
    color: Colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: 0.8,
  },
  suggestions: { flexDirection: 'row', flexWrap: 'wrap', gap: Spacing.sm },
  chip: {
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.xs + 2,
    borderRadius: Radius.full,
    backgroundColor: Colors.surfaceSubtle,
    borderWidth: 1.5,
    borderColor: Colors.border,
  },
  chipActive: { backgroundColor: Colors.leafGreen, borderColor: Colors.leafGreen },
  chipText: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.textSecondary },
  chipTextActive: { color: Colors.white },
  footer: { padding: Spacing.lg },
  button: {
    backgroundColor: Colors.leafGreen,
    borderRadius: Radius.lg,
    paddingVertical: Spacing.md,
    alignItems: 'center',
  },
  buttonDisabled: { opacity: 0.4 },
  buttonText: {
    fontFamily: Typography.fontHeadingSemi,
    fontSize: Typography.size.md,
    color: Colors.white,
  },
});
