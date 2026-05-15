import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/api/client';
import type { CatalogItem } from '@/types/api';

interface ShopCatalog {
  items: CatalogItem[];
  featured: CatalogItem[];
}

export function useShopCatalog() {
  return useQuery({
    queryKey: ['shop', 'catalog'],
    queryFn: () => api.get<ShopCatalog>('/v1/shop/catalog'),
    staleTime: 5 * 60_000,
  });
}

export function usePurchaseItem() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (catalog_item_id: string) =>
      api.post('/v1/shop/purchase', { catalog_item_id }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['shop', 'catalog'] });
      qc.invalidateQueries({ queryKey: ['home', 'state'] });
    },
  });
}

export function useEquipItem() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (inventory_id: string) =>
      api.post('/v1/shop/equip', { inventory_id }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['companion', 'state'] }),
  });
}
