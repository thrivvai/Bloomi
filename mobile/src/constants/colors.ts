export const Colors = {
  leafGreen: '#6FAF7B',
  bloomCoral: '#F28C7B',
  skyCream: '#FFF7F0',
  deepMoss: '#294B45',
  softClay: '#C9856B',

  white: '#FFFFFF',
  black: '#1A1A1A',
  textPrimary: '#294B45',
  textSecondary: '#6B7F79',
  textMuted: '#A8B8B4',

  surfaceCard: '#FFFFFF',
  surfaceSubtle: '#F5EFE8',
  border: '#E8DDD6',

  success: '#6FAF7B',
  warning: '#F5C842',
  error: '#E87070',
} as const;

export type ColorKey = keyof typeof Colors;
