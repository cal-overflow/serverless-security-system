<template>
  <div class="max-w-screen-lg mx-auto">
    <div class="bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
      <p class="text-2xl font-bold">
        Users

        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
        </svg>
      </p>
    </div>
    <div class="p-4 sm:grid grid-cols-2 lg:grid-cols-3 flex-nowrap">
      <user-card
        v-for="user in users"
        :key="`user-${user.name}`"
        :user="user"
        :can-edit="authenticatedUser.admin || isAuthenticatedAsUser(user)"
        :is-authenticated="isAuthenticatedAsUser(user)"
      />
      <!-- Extra user card for inviting users -->
      <user-card
        v-if="authenticatedUser.admin"
      />
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
  asyncData({ user }) {
    return { authenticatedUser: user };
  },
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
    },
    isAuthenticatedAsUser(user) {
      return this.authenticatedUser.name === user.name;
    }
  }
}
</script>

