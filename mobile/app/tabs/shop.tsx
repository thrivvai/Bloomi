import { ActivityIndicator, Alert, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors } from '@/constants/colors';
import { Radius, Shadow, Spacing, Typography } from '@/constants/theme';
import { useShopCatalog, usePurchaseItem } from '@/hooks/useShop';
import type { CatalogItem } from '@/types/api';

const RARITY_COLOR: Record<string, string> = {
  common: Colors.textMuted,
  rare: Colors.bloomCoral,
  legendary: Colors.softClay,
};

const TYPE_EMOJI: Record<string, string> = {
  outfit: '👕',
  accessory: '✨',
  pot: '🪴',
  background: '🖼️',
  room_item: '🏡',
  theme: '🎨',
};

function ItemCard({ item }: { item: CatalogItem }) {
  const purchase = usePurchaseItem();

  async function handleBuy() {
    try {
      await purchase.mutateAsync(item.id);
      Alert.alert('Got it!', `${item.name} is now in your collection.`);
    } catch (e: any) {
      Alert.alert('Could not purchase', e.message ?? 'Something went wrong.');
    }
  }

  return (
    <View style={styles.itemCard}>
      <View style={styles.itemIcon}>
        <Text style={styles.itemEmoji}>{TYPE_EMOJI[item.item_type] ?? '🎁'}</Text>
      </View>
      <View style={{ flex: 1 }}>
        <Text style={styles.itemName}>{item.name}</Text>
        <Text style={[styles.itemRarity, { color: RARITY_COLOR[item.rarity] ?? Colors.textMuted }]}>
          {item.rarity}
        </Text>
      </View>
      <TouchableOpacity
        style={[styles.buyBtn, purchase.isPending && styles.buyBtnDisabled]}
        onPress={handleBuy}
        disabled={purchase.isPending}
      >
        <Text style={styles.buyBtnText}>
          {item.price_amount === 0 ? 'Free' : `${item.price_amount} ${item.price_currency}`}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

export default function ShopScreen() {
  const { data, isLoading } = useShopCatalog();

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
        <Text style={styles.screenTitle}>Closet & Garden</Text>
        <Text style={styles.screenSub}>Make your Bloomi yours.</Text>

        {data?.featured && data.featured.length > 0 && (
          <>
            <Text style={styles.sectionLabel}>Featured</Text>
            {data.featured.map((item) => <ItemCard key={item.id} item={item} />)}
          </>
        )}

        {data?.items && data.items.length > 0 && (
          <>
            <Text style={styles.sectionLabel}>All items</Text>
            {data.items.map((item) => <ItemCard key={item.id} item={item} />)}
          </>
        )}

        {(!data?.items || data.items.length === 0) && (
          <View style={styles.emptyState}>
            <Text style={styles.emptyEmoji}>🛍️</Text>
            <Text style={styles.emptyText}>New items coming soon.</Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.skyCream },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: Colors.skyCream },
  scroll: { paddingHorizontal: Spacing.lg, paddingBottom: Spacing['3xl'], gap: Spacing.sm, paddingTop: Spacing.lg },
  screenTitle: { fontFamily: Typography.fontHeading, fontSize: Typography.size.xl, color: Colors.textPrimary },
  screenSub: { fontFamily: Typography.fontBody, fontSize: Typography.size.base, color: Colors.textSecondary, marginBottom: Spacing.sm },
  sectionLabel: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.textMuted, textTransform: 'uppercase', letterSpacing: 0.8, marginTop: Spacing.md },
  itemCard: {
    backgroundColor: Colors.white,
    borderRadius: Radius.lg,
    padding: Spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.sm,
    ...Shadow.soft,
  },
  itemIcon: { width: 44, height: 44, borderRadius: Radius.md, backgroundColor: Colors.surfaceSubtle, alignItems: 'center', justifyContent: 'center' },
  itemEmoji: { fontSize: 24 },
  itemName: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.base, color: Colors.textPrimary },
  itemRarity: { fontFamily: Typography.fontBody, fontSize: Typography.size.sm, textTransform: 'capitalize', marginTop: 2 },
  buyBtn: { backgroundColor: Colors.leafGreen, borderRadius: Radius.full, paddingHorizontal: Spacing.md, paddingVertical: Spacing.xs + 2 },
  buyBtnDisabled: { opacity: 0.5 },
  buyBtnText: { fontFamily: Typography.fontBodyMedium, fontSize: Typography.size.sm, color: Colors.white },
  emptyState: { alignItems: 'center', paddingVertical: Spacing['2xl'], gap: Spacing.sm },
  emptyEmoji: { fontSize: 48 },
  emptyText: { fontFamily: Typography.fontBody, fontSize: Typography.size.base, color: Colors.textMuted, textAlign: 'center' },
});
