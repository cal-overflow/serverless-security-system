<template>
  <div>
    <p class="text-4xl font-bold">Signing you out...</p>
  </div>
</template>

<script>
import { logout } from '@/services/auth.js';

export default {
  name: 'LogoutPage',
  layout: 'gateway',
  asyncData({ redirect }) {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      return redirect('/login');
    }

    logout()
    .then(() => {
      return redirect('/login');
    })
    .catch(() => {
      return redirect('/login');
    });
  }
}
</script>
