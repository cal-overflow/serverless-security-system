
<template>
  <div class="max-w-screen-lg mx-auto bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <form @submit.prevent="postUser">
      <label for="name">Name</label>
      <input
        v-model="name"
        type="text"
        name="name"
        id="name"
        required
        class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
      />

      <label for="pin">Pin</label>
      <input
        v-model="pin"
        type="password"
        name="pin"
        id="pin"
        required
        class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
      />

      <label for="admin">Admin</label>
      <input
        v-model="admin"
        type="checkbox"
        name="admin"
        id="admin"
      />
      <input
        type="submit"
        value="Login"
        :class="`rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white transition duration-1000 ${name && pin ? 'opacity-1 cursor-pointer' : 'opacity-25 cursor-default'}`"
      />
    </form>
  </div>
</template>


<script>
import { createUser } from '@/services/users.js';

export default {
  name: 'user-card',
  data: () => ({
    name: '',
    pin: '',
    admin: false,
  }),
  methods: {
    postUser() {
      const user = {
        name: this.name,
        pin: this.pin,
        admin: this.admin
      };

      createUser(user)
      .then(() => {
        this.$emit('userCreated', user)
      })
      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
      })
      .finally(() => {
        this.isLoading = false;
      });
    },
  }
}
</script>

