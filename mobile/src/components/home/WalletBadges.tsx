import { StyleSheet, Text, View } from 'react-native';
import { Colors } from '@/constants/colors';
import { Radius, Spacing, Typography } from '@/constants/theme';
import type { WalletBalance } from '@/types/api';

const WALLET_EMOJI: Record<string, string> = {
  energy: '⚡',
  coins: '🪙',
};

interface Props {
  balances: WalletBalance[];
}

export function WalletBadges({ balances }: Props) {
  return (
    <View style={styles.row}>
      {balances.map((w) => (
        <View key={w.wallet_type} style={styles.badge}>
          <Text style={styles.emoji}>{WALLET_EMOJI[w.wallet_type] ?? '💎'}</Text>
          <Text style={styles.amount}>{w.balance}</Text>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', gap: Spacing.xs },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: Colors.white,
    borderRadius: Radius.full,
    paddingHorizontal: Spacing.sm,
    paddingVertical: 4,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  emoji: { fontSize: 14 },
  amount: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.textPrimary },
});
