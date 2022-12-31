<template>
  <Tutorial />
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
      return redirect('/login');
    });
  }
}
</script>
