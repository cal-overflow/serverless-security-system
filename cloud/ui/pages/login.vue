<template>
  <div class="mx-auto flex h-screen">
    <div class="max-w-screen-sm m-auto w-full bg-card-light dark:bg-card-dark p-4 flex flex-wrap shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
      <p class="text-2xl font-bold">Login</p>
      <form @submit.prevent="submitLogin" class="flex flex-wrap w-full">
        <label for="username">User</label>
        <input
          v-model="username"
          type="text"
          name="username"
          id="username"
          required
          :disabled="infoMessage === 'Loading...'"
          class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light focus:dark:ring-primary-dark transition"
        />

        <label for="password">Pin</label>
        <input
          v-model="password"
          type="password"
          name="password"
          id="password"
          required
          :disabled="infoMessage === 'Loading...'"
          class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light focus:dark:ring-primary-dark transition"
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
  data: () => ({
    username: '',
    password: '',
    infoMessage: ''
  }),
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
