<template>
  <div>
    <grid-view title="Users">
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
        v-if="!isLoading && authenticatedUser.admin"
      />
    </grid-view>

    <overlay v-if="userBeingEdited" title="Edit user" v-on:close="userBeingEdited = undefined">
      <p>Editing user {{userBeingEditedWithoutChanges.name}}</p>
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
          minlength="4"
          maxlength="64"
          id="password"
          :disabled="isSavingChanges"
          class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
        />

        <div v-if="authenticatedUser.admin">
          <label for="admin" class="text-lg">Admin</label>
          <toggle v-model="userBeingEdited.admin" :showLabel="true" onLabel="Yes" offLabel="No" />
          <button @click="promptDeleteUser()" class="my-4 underline hover:no-underline transition duration-1000">Delete user</button>
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
        // Put the authenticated user at the front of the users array
        users.sort((a, b) => a.name === this.authenticatedUser.name ? -1 : b.name === this.authenticatedUser.name ? 1 : 0);
        this.users = users;
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
