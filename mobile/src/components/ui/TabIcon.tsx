import { StyleSheet, Text, View } from 'react-native';
import { Colors } from '@/constants/colors';

const ICONS: Record<string, { active: string; inactive: string }> = {
  home:     { active: '🏡', inactive: '🏠' },
  goals:    { active: '✅', inactive: '☑️' },
  journal:  { active: '📓', inactive: '📔' },
  shop:     { active: '🛍️', inactive: '🛒' },
  insights: { active: '✨', inactive: '⭐' },
};

interface Props {
  name: string;
  color: string;
  focused: boolean;
}

export function TabIcon({ name, focused }: Props) {
  const icon = ICONS[name] ?? { active: '●', inactive: '○' };
  return (
    <View style={styles.container}>
      <Text style={styles.emoji}>{focused ? icon.active : icon.inactive}</Text>
      {focused && <View style={styles.dot} />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { alignItems: 'center', gap: 4 },
  emoji: { fontSize: 24 },
  dot: { width: 4, height: 4, borderRadius: 2, backgroundColor: Colors.leafGreen },
});
