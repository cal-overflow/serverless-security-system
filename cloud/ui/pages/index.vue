<template>
  <div>
    <p class="text-4xl font-bold">Security System</p>
    <video-feed type="motion" />
    <client-overview />
    <footer-bar />
  </div>
</template>

<script>
import { refreshToken } from '@/services/auth.js';

export default {
  name: 'IndexPage',
  asyncData({ redirect }) {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      return redirect('/login');
    }

    // check if token is valid (attempt to refresh)
    refreshToken()
    .catch(() => {
      console.log('redirecting to login?')
      return redirect('/login');
    });
  }
}
</script>
