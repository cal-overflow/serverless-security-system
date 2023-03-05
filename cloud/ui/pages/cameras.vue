<template>
  <div class="max-w-screen-lg mx-auto">
    <div class="bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
      <div>
        <p class="text-2xl font-bold">Cameras</p>
      </div>
    </div>
    <div class="p-4 sm:grid grid-cols-2 lg:grid-cols-3 flex-nowrap">
      <camera-card
        v-for="camera in cameras"
        :key="`camera-${camera.id}`"
        :camera="camera"
        :can-edit="authenticatedUser.admin"
        v-on:edit="editCamera(camera)"
      />
    </div>
    <overlay v-if="cameraBeingEdited" title="Edit camera" v-on:close="cameraBeingEdited = undefined">
      <p>Editing camera with id <code>{{cameraBeingEditedWithoutChanges.id}}</code></p>
      <form @submit.prevent="saveChanges" class="flex flex-wrap w-full">
        <label for="name" class="text-lg">Camera name</label>
        <input
          v-model="cameraBeingEdited.name"
          type="text"
          name="name"
          id="name"
          maxlength="40"
          :disabled="isSavingChanges"
          class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
          autocorrect="off"
          autocapitalize="none"
        />

        <label for="motion_threshold" class="text-lg">Motion threshold</label>
        <select
          v-model="cameraBeingEdited.motion_threshold"
          name="motion_threshold"
          :disabled="isSavingChanges"
          class="appearance-none w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
        >
          <option value="15000">Lowest sensitivity (15000)</option>
          <option value="10000">Low sensitivity (10000)</option>
          <option value="7500">Moderate sensitivity (7500)</option>
          <option value="5000">High sensitivity (5000)</option>
          <option value="2500">Highest sensitivity (2500)</option>
        </select>

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
  </div>
</template>


<script>
import { editClient, getClients } from '@/services/clients.js';

export default {
  name: 'CamerasPage',
  middleware: 'authenticate',
  data: () => ({
    cameras: [],
    isLoading: true,
    isSavingChanges: false,
    infoMessage: '',
    cameraBeingEdited: undefined,
    cameraBeingEditedWithoutChanges: undefined,
  }),
  asyncData({ user }) {
    return { authenticatedUser: user };
  },
  mounted() {
    this.getClients();
  },
  methods: {
   getClients() {
      this.isLoading = true;

      getClients()
      .then((cameras) => {
        this.cameras = cameras;
      })
      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
      })
      .finally(() => {
        this.isLoading = false;
      });
    },
    editCamera(camera) {
      this.cameraBeingEdited = { ...camera };
      this.cameraBeingEditedWithoutChanges = { ...camera };
    },
    saveChanges() {
      this.infoMessage = "Saving changes...";
      this.isSavingChanges = true;

      editClient(this.cameraBeingEdited)
      .then(() => {
        this.infoMessage = '';
        this.cameraBeingEdited = undefined;
        this.getClients();
      })
      .catch((err) => {
        this.infoMessage = err.message;
      })
      .finally(() => {
        this.isSavingChanges = false;
      });
    },
  },
  computed: {
    hasChanges() {
      return JSON.stringify(this.cameraBeingEdited) !== JSON.stringify(this.cameraBeingEditedWithoutChanges);
    },
  },
}
</script>

