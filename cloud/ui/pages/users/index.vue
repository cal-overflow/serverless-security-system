<template>
  <div class="max-w-screen-lg mx-auto bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <div>
      <p class="text-2xl font-bold">Users</p>
    </div>
    <div class="flex flex-wrap md:flex-nowrap">
      <nuxt-link
        v-for="user in users"
        :key="`user-${user.name}`"
        :to="`/users/${user.name}`"
      >
        <user-card
          :user="user"
        />
      </nuxt-link>
      <create-user-card v-if="isAddingUser" @userCreated="addUser" />
      <button
        v-else
        class="rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white"
        @click="isAddingUser = true"
      >
        Create User
      </button>
    </div>
  </div>
</template>


<script>
import { getUsers } from '@/services/users.js';

export default {
  name: 'UsersPage',
  middleware: 'authenticate',
  data: () => ({
    users: [],
    isLoading: true,
    isAddingUser: false,
  }),
  mounted() {
    this.isLoading = true;

    getUsers()
    .then((users) => {
      this.users = users;
      console.log(users)
    })
    .catch((err) => {
      // TODO - implement error handling
      console.log(err);
    })
    .finally(() => {
      this.isLoading = false;
    });
  },
  methods: {
    addUser(user) {
      this.isAddingUser = false;
      this.users.push(user);
    } 
  }
}
</script>

