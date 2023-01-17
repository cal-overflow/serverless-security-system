<template>
  <div class="mx-auto flex h-screen">
    <div class="max-w-screen-sm m-auto w-full sm:bg-card-light sm:dark:bg-card-dark p-8 sm:p-4 flex flex-wrap sm:shadow-lg sm:dark:shadow-shadow-dark sm:hover:shadow-none sm:hover:rounded motion-safe:animate-fade-in-fast transition">
      <p class="text-3xl font-bold">Login</p>
      <form @submit.prevent="submitLogin" class="flex flex-wrap w-full">
        <label for="username" class="text-lg">User</label>
        <input
          v-model="username"
          type="text"
          name="username"
          id="username"
          required
          :disabled="infoMessage === 'Loading...'"
          class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
        />

        <label for="password" class="text-lg">Pin</label>
        <input
          v-model="password"
          type="password"
          name="password"
          id="password"
          required
          :disabled="infoMessage === 'Loading...'"
          class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
        />

        <div class="flex justify-between w-full">
          <p class="text-sm my-auto">{{infoMessage}}</p>
          <input
            type="submit"
            value="Login"
            :class="`rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white transition duration-1000 ${username && password ? 'opacity-1 cursor-pointer' : 'opacity-25 cursor-default'}`"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { login } from '@/services/auth.js';

export default {
  name: 'LoginPage',
  layout: 'gateway',
  data: () => ({
    username: '',
    password: '',
    infoMessage: ''
  }),
  asyncData({ redirect }) {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      redirect('/');
    }
  },
  methods: {
    submitLogin() {
      this.infoMessage = 'Loading...';
      const credentials = {
        name: this.username,
        pin: this.password,
      };

      login(credentials)
        .then(() => {
          this.$router.push('/');
        })
        .catch((err) => {
          this.infoMessage = err.message;
        });
    }
  },
  watch: {
    username() {
      this.infoMessage = '';
    },
    password() {
      this.infoMessage = '';
    }
  }
}
</script>
