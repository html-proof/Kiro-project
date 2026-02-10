// Premium Aurora Dark Theme
export const colors = {
  // Background
  background: '#000000',
  backgroundCard: '#121212',
  backgroundElevated: '#1a1a1a',
  
  // Aurora Gradient
  auroraPurple: '#8B5CF6',
  auroraCyan: '#06B6D4',
  auroraPink: '#EC4899',
  
  // Accent
  primary: '#1DB954',
  primaryDark: '#1aa34a',
  
  // Text
  textPrimary: '#FFFFFF',
  textSecondary: '#B3B3B3',
  textTertiary: '#6B7280',
  
  // Glass
  glassBackground: 'rgba(18, 18, 18, 0.8)',
  glassBorder: 'rgba(255, 255, 255, 0.1)',
  
  // Status
  success: '#10B981',
  error: '#EF4444',
  warning: '#F59E0B',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const borderRadius = {
  sm: 8,
  md: 16,
  lg: 20,
  xl: 28,
  full: 9999,
};

export const typography = {
  h1: {
    fontSize: 32,
    fontWeight: 'bold',
    color: colors.textPrimary,
  },
  h2: {
    fontSize: 24,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  h3: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  body: {
    fontSize: 16,
    fontWeight: '400',
    color: colors.textPrimary,
  },
  caption: {
    fontSize: 14,
    fontWeight: '400',
    color: colors.textSecondary,
  },
  small: {
    fontSize: 12,
    fontWeight: '400',
    color: colors.textTertiary,
  },
};

export const shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 2,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 4.65,
    elevation: 4,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height 6 },
    shadowOpacity: 0.37,
    shadowRadius: 7.49,
    elevation: 8,
  },
  glow: {
    shadowColor: colors.auroraCyan,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 10,
    elevation: 10,
  },
};

// Mood colors
export const moodColors = {
  romantic: ['#EC4899', '#F472B6'],
  party: ['#EF4444', '#F97316'],
  chill: ['#06B6D4', '#0EA5E9'],
  workout: ['#F59E0B', '#EAB308'],
  sleep: ['#8B5CF6', '#A78BFA'],
  sad: ['#6B7280', '#9CA3AF'],
  devotional: ['#F59E0B', '#FBBF24'],
  motivational: ['#10B981', '#34D399'],
};
