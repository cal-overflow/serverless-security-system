<template>
  <div class="max-w-screen-lg mx-auto bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <div>
      <p class="text-2xl font-bold">User</p>
    </div>
    <div class="flex flex-wrap md:flex-nowrap">
      <user-card
        v-if="user"
        :user="user"
      />
      <create-user-card v-if="isAddingUser" @userCreated="addUser" />
      <button
        v-else
        class="rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white"
        @click="isEditingUser = true"
      >
        Edit User
      </button>
    </div>
  </div>
</template>


<script>
import { getUser } from '@/services/users.js';

export default {
  name: 'UserPage',
  middleware: 'authenticate',
  async asyncData({ params, error }) {
    const userName = params.pathMatch;

    const user = await getUser(userName)
      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
      });

    return { user, isLoading: false };
  },
  data: () => ({
    isEditingUser: false,
  }),
  methods: {
    updateUser(updatedUser) {
      this.isEditingUser = false;
      this.user = updatedUser;
    } 
  }
}
</script>

