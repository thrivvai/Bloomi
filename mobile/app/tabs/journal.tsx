import { useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors } from '@/constants/colors';
import { Radius, Shadow, Spacing, Typography } from '@/constants/theme';
import { useCreateJournalEntry } from '@/hooks/useJournal';

const PROMPTS = [
  'What felt heavy today, and what felt light?',
  'What\'s one small thing you did for yourself?',
  'What are you holding onto that you could gently put down?',
  'What made you smile, even briefly?',
  'What does your body need right now?',
];

export default function JournalScreen() {
  const [body, setBody] = useState('');
  const [selectedPrompt, setSelectedPrompt] = useState<string | null>(null);
  const createEntry = useCreateJournalEntry();

  const promptIndex = Math.floor(Date.now() / 86_400_000) % PROMPTS.length;
  const todayPrompt = PROMPTS[promptIndex];

  function usePrompt(prompt: string) {
    setSelectedPrompt(prompt);
    setBody('');
  }

  async function handleSave() {
    if (!body.trim()) return;
    try {
      await createEntry.mutateAsync({
        body_text: body.trim(),
        entry_type: selectedPrompt ? 'guided' : 'free',
        prompt_id: selectedPrompt ?? undefined,
      });
      Alert.alert('Saved', 'Your reflection was saved. Your Bloomi holds space for you. 🌿');
      setBody('');
      setSelectedPrompt(null);
    } catch {
      Alert.alert('Could not save', 'Please try again in a moment.');
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <ScrollView
          contentContainerStyle={styles.scroll}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          <Text style={styles.screenTitle}>Reflect</Text>
          <Text style={styles.screenSub}>No pressure. A few words is enough.</Text>

          {/* Daily prompt */}
          <View style={styles.promptCard}>
            <Text style={styles.promptLabel}>Today's prompt</Text>
            <Text style={styles.promptText}>{todayPrompt}</Text>
            <TouchableOpacity
              style={styles.usePromptBtn}
              onPress={() => usePrompt(todayPrompt)}
            >
              <Text style={styles.usePromptText}>Use this prompt</Text>
            </TouchableOpacity>
          </View>

          {selectedPrompt && (
            <View style={styles.selectedPrompt}>
              <Text style={styles.selectedPromptText}>"{selectedPrompt}"</Text>
            </View>
          )}

          <TextInput
            style={styles.textArea}
            value={body}
            onChangeText={setBody}
            placeholder={selectedPrompt ? 'Write freely…' : 'What\'s on your mind?'}
            placeholderTextColor={Colors.textMuted}
            multiline
            textAlignVertical="top"
            maxLength={10000}
          />
        </ScrollView>

        <View style={styles.footer}>
          <TouchableOpacity
            style={[styles.saveBtn, (!body.trim() || createEntry.isPending) && styles.saveBtnDisabled]}
            onPress={handleSave}
            disabled={!body.trim() || createEntry.isPending}
          >
            {createEntry.isPending ? (
              <ActivityIndicator color={Colors.white} />
            ) : (
              <Text style={styles.saveBtnText}>Save reflection</Text>
            )}
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.skyCream },
  scroll: { paddingHorizontal: Spacing.lg, paddingBottom: Spacing['2xl'], gap: Spacing.md, paddingTop: Spacing.lg },
  screenTitle: { fontFamily: Typography.fontHeading, fontSize: Typography.size.xl, color: Colors.textPrimary },
  screenSub: { fontFamily: Typography.fontBody, fontSize: Typography.size.base, color: Colors.textSecondary },
  promptCard: {
    backgroundColor: Colors.deepMoss,
    borderRadius: Radius.xl,
    padding: Spacing.lg,
    gap: Spacing.sm,
    ...Shadow.card,
  },
  promptLabel: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.xs, color: Colors.leafGreen, textTransform: 'uppercase', letterSpacing: 0.8 },
  promptText: { fontFamily: Typography.fontHeadingSemi, fontSize: Typography.size.md, color: Colors.white, lineHeight: Typography.size.md * 1.5 },
  usePromptBtn: { alignSelf: 'flex-start', marginTop: Spacing.xs, paddingHorizontal: Spacing.md, paddingVertical: Spacing.xs, backgroundColor: Colors.leafGreen + '33', borderRadius: Radius.full },
  usePromptText: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.leafGreen },
  selectedPrompt: { backgroundColor: Colors.surfaceSubtle, borderRadius: Radius.lg, padding: Spacing.md, borderLeftWidth: 3, borderLeftColor: Colors.leafGreen },
  selectedPromptText: { fontFamily: Typography.fontBody, fontSize: Typography.size.sm, color: Colors.textSecondary, fontStyle: 'italic' },
  textArea: {
    backgroundColor: Colors.white,
    borderRadius: Radius.xl,
    borderWidth: 1.5,
    borderColor: Colors.border,
    padding: Spacing.md,
    fontFamily: Typography.fontBody,
    fontSize: Typography.size.base,
    color: Colors.textPrimary,
    lineHeight: Typography.size.base * 1.7,
    minHeight: 180,
  },
  footer: { padding: Spacing.lg },
  saveBtn: { backgroundColor: Colors.leafGreen, borderRadius: Radius.lg, paddingVertical: Spacing.md, alignItems: 'center' },
  saveBtnDisabled: { opacity: 0.4 },
  saveBtnText: { fontFamily: Typography.fontHeadingSemi, fontSize: Typography.size.md, color: Colors.white },
});
