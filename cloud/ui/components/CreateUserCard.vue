<template>
  <div @mouseover="mouseover = true" @mouseleave="mouseover = false" class="bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <div>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-24 h-24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M19 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM4 19.235v-.11a6.375 6.375 0 0112.75 0v.109A12.318 12.318 0 0110.374 21c-2.331 0-4.512-.645-6.374-1.766z" />
      </svg>
      <p class="text-xl font-bold">
        Add user
      </p>
      <button v-if="mouseover">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />
        </svg>
      </button>
      <!--
      <p class="text-md"><span class="font-bold">Pin:</span>pin</p>
      <p class="text-md"><span class="font-bold">Admin:</span>admin</p>
      -->
    </div>
  </div>
</template>


<script>
export default {
  name: 'create-user-card',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    mouseover: false
  }),
  computed: {
    pin() {
      return this.user.pin || '****';
    }
  },
}
</script>


<!--
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
-->
