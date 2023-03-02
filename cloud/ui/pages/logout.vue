<template>
  <div class="mx-auto flex h-screen">
    <div class="max-w-screen-sm m-auto w-full sm:bg-card-light sm:dark:bg-card-dark p-8 sm:p-4 flex flex-wrap sm:shadow-lg sm:dark:shadow-shadow-dark sm:hover:shadow-none sm:hover:rounded motion-safe:animate-fade-in-fast transition animate-pulse">
      <p class="text-3xl font-bold">Signing you out...</p>

      <form class="flex flex-wrap w-full">
        <label for="lazyUsername" class="text-lg">User</label>
        <input
          name="lazyUsername"
          disabled
          class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
        />

        <label for="lazyPassword" class="text-lg">Pin</label>
        <input
          name="lazyPassword"
          disabled
          class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
        />

        <div class="flex justify-between w-full">
          <p class="text-sm my-auto"></p>
          <input
            type="submit"
            value="Login"
            disabled
            class="rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white transition opacity-25 cursor-default"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { logout } from '@/services/auth.js';

export default {
  name: 'LogoutPage',
  layout: 'gateway',
  asyncData({ redirect, route }) {
    const accessToken = localStorage.getItem('accessToken');

    let redirectPath = '/login';
    if (route.query.redirectPath) {
      redirectPath = `/login?redirectPath=${route.query.redirectPath}`
    }

    if (!accessToken) {
      return redirect(redirectPath);
    }

    logout()
    .then(() => {
      return redirect(redirectPath);
    })
    .catch(() => {
      return redirect(redirectPath);
    });
  }
}
</script>
