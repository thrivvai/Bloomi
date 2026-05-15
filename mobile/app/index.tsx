import { Redirect } from 'expo-router';
import { useAuthStore } from '@/store/authStore';

export default function Root() {
  const { userId, isOnboarded } = useAuthStore();

  if (!userId || !isOnboarded) {
    return <Redirect href="/onboarding/choose" />;
  }

  return <Redirect href="/tabs" />;
}
