<template>
  <div>
    <grid-view title="Cameras">
      <camera-card
        v-for="camera in cameras"
        :key="`camera-${camera.id}`"
        :camera="camera"
        :can-edit="authenticatedUser.admin"
        @edit="editCamera(camera)"
      />
    </grid-view>
    <overlay
      v-if="cameraBeingEdited"
      title="Edit camera"
      @close="cameraBeingEdited = undefined"
    >
      <p>
        Editing camera with id
        <code>{{ cameraBeingEditedWithoutChanges.id }}</code>
      </p>
      <form class="flex flex-wrap w-full" @submit.prevent="saveChanges">
        <label for="name" class="text-lg">Camera name</label>
        <input
          id="name"
          v-model="cameraBeingEdited.name"
          type="text"
          name="name"
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

        <div v-if="authenticatedUser.admin">
          <label for="admin" class="text-lg">Status</label>
          <toggle
            v-model="cameraBeingEdited.is_active"
            :show-label="true"
            on-label="Active"
            off-label="Inactive"
          />
        </div>

        <div class="flex justify-between w-full">
          <p class="text-sm my-auto">{{ infoMessage }}</p>
          <input
            type="submit"
            value="Save changes"
            :class="`rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white transition duration-1000 ${
              hasChanges && !isSavingChanges
                ? 'opacity-1 cursor-pointer'
                : 'opacity-25 cursor-default'
            }`"
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
  async asyncData({ user }) {
    const clients = await getClients().catch((err) => {
      // TODO - implement error handling
      console.log(err);
    });

    // Put the active clients at the front of the array
    clients.sort((a, b) => (a.is_active ? -1 : b.is_active ? 1 : 0));

    return { cameras: clients, authenticatedUser: user };
  },
  data: () => ({
    cameras: [],
    isSavingChanges: false,
    infoMessage: '',
    cameraBeingEdited: undefined,
    cameraBeingEditedWithoutChanges: undefined,
  }),
  computed: {
    hasChanges() {
      return (
        JSON.stringify(this.cameraBeingEdited) !==
        JSON.stringify(this.cameraBeingEditedWithoutChanges)
      );
    },
  },
  methods: {
    editCamera(camera) {
      this.cameraBeingEdited = { ...camera };
      this.cameraBeingEditedWithoutChanges = { ...camera };
    },
    saveChanges() {
      this.infoMessage = 'Saving changes...';
      this.isSavingChanges = true;

      const changes = {
        ...this.cameraBeingEdited,
        motion_threshold: parseInt(this.cameraBeingEdited.motion_threshold),
      };

      editClient(changes)
        .then(() => {
          this.infoMessage = '';
          this.cameraBeingEdited = undefined;
          this.$nuxt.refresh(); // refresh asyncData
        })
        .catch((err) => {
          this.infoMessage = err.message;
        })
        .finally(() => {
          this.isSavingChanges = false;
        });
    },
  },
};
</script>
