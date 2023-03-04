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
        v-on:edit="editUser(user)"
      />
      <!-- Extra user card for inviting users -->
      <user-card
        v-if="authenticatedUser.admin"
      />
    </div>

    <overlay v-if="userBeingEdited" :title="`Edit user ${userBeingEditedWithoutChanges.name}`" v-on:close="userBeingEdited = undefined">
      <form @submit.prevent="saveChanges" class="flex flex-wrap w-full">
        <label for="username" class="text-lg">Username</label>
        <input
          v-model="userBeingEdited.name"
          type="text"
          name="username"
          id="username"
          :disabled="isSavingChanges"
          class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
          autocorrect="off"
          autocapitalize="none"
        />

        <label for="password" class="text-lg">Pin</label>
        <input
          v-model="userBeingEdited.pin"
          type="password"
          name="password"
          id="password"
          :disabled="isSavingChanges"
          class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
        />

        <div v-if="authenticatedUser.admin">
          <label for="admin" class="text-lg">Admin</label>
          <toggle v-model="userBeingEdited.admin" :showLabel="true" onLabel="Yes" offLabel="No" />
          <button @click="promptDeleteUser()" class="rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white transition duration-1000">Delete</button>
        </div>

        <div class="flex justify-between w-full">
          <p class="text-sm my-auto">{{infoMessage}}</p>
          <input
            type="submit"
            value="Save changes"
            :class="`rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white transition duration-1000 ${hasChanges && !isSavingChanges ? 'opacity-1 cursor-pointer' : 'opacity-25 cursor-default'}`"
          />
        </div>
      </form>
    </overlay>
    <confirmation
      v-if="userBeingDeleted"
      :title="`Delete ${userBeingDeleted.name}`"
      v-on:confirm="deleteUser"
      v-on:deny="userBeingDeleted = undefined"
      v-on:close="userBeingDeleted = undefined"
    >
      <p>Are you sure you want to delete {{userBeingDeleted.name}}? This action cannot be undone.</p>
      <p>{{infoMessage}}</p>
    </confirmation>
  </div>
</template>


<script>
import { deleteUser, editUser, getUsers } from '@/services/users.js';

export default {
  name: 'UsersPage',
  middleware: 'authenticate',
  data: () => ({
    users: [],
    isLoading: true,
    userBeingEdited: undefined,
    userBeingEditedWithoutChanges: undefined,
    userBeingDeleted: undefined,
    isSavingChanges: false,
    infoMessage: ''
  }),
  asyncData({ user }) {
    return { authenticatedUser: user };
  },
  mounted() {
    this.getUsers();
  },
  methods: {
    getUsers() {
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
    editUser(user) {
      this.userBeingEdited = { ...user };
      this.userBeingEditedWithoutChanges = { ...user };
    },
    saveChanges() {
      this.infoMessage = "Saving changes...";
      this.isSavingChanges = true;
      const editedUser = {
        pin: this.userBeingEdited.pin,
      };

      if (this.userBeingEditedWithoutChanges.name !== this.userBeingEdited.name) {
        editedUser.name = this.userBeingEdited.name;
      }
      if (this.authenticatedUser.admin && this.userBeingEditedWithoutChanges.admin !== this.userBeingEdited.admin) {
        editedUser.admin = this.userBeingEdited.admin;
      }

      editUser(this.userBeingEditedWithoutChanges.name, editedUser)
      .then(() => {
        this.infoMessage = '';
        this.userBeingEdited = undefined;
        this.getUsers();
      })
      .catch((err) => {
        this.infoMessage = err.message;
      })
      .finally(() => {
        this.isSavingChanges = false;
      });
    },
    promptDeleteUser() {
      this.userBeingDeleted = { ...this.userBeingEdited };
      this.userBeingEdited = undefined;
    },
    deleteUser() {
      this.infoMessage = "Loading...";
      deleteUser(this.userBeingDeletedWithoutChanges.name)
      .then(() => {
        this.infoMessage = '';
        this.userBeingDeleted = undefined;
        this.getUsers();
      })
      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
        this.infoMessage = err.message;
      })
      
    },
    isAuthenticatedAsUser(user) {
      return this.authenticatedUser.name === user.name;
    }
  },
  computed: {
    hasChanges() {
      return JSON.stringify(this.userBeingEdited) !== JSON.stringify(this.userBeingEditedWithoutChanges);
    }
  }
}
</script>

