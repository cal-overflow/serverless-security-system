<template>
  <div class="max-w-screen-lg mx-auto bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <div>
      <p class="text-2xl font-bold">Camera</p>
    </div>
    <div class="flex flex-wrap md:flex-nowrap">
      <camera-card
        v-if="camera"
        :camera="camera"
      />
      <button
        v-else
        class="rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white"
        @click="isEditingCamera = true"
      >
        Edit Camera
      </button>
    </div>
  </div>
</template>


<script>
import { getClient } from '@/services/clients.js';

export default {
  name: 'CameraPage',
  middleware: 'authenticate',
  async asyncData({ params, error }) {
    const clientId = params.pathMatch;

    const camera = await getClient(clientId)
      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
      });

    return { camera, isLoading: false };
  },
  data: () => ({
    isEditingCamera: false,
  }),
  methods: {
    updateCamera(updatedCamera) {
      this.isEditingCamera = false;
      this.camera = updatedCamera;
    } 
  }
}
</script>

