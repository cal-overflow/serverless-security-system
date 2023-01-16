<template>
  <div class="max-w-screen-lg mx-auto bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <div>
      <p class="text-2xl font-bold">Cameras</p>
    </div>
    <div class="flex flex-wrap md:flex-nowrap">
      <nuxt-link  
        v-for="camera in cameras"
        :key="`camera-${camera.id}`"
        :to="`/cameras/${camera.id}`"
      >
        <camera-card
          :camera="camera"
        />
      </nuxt-link>
    </div>
  </div>
</template>


<script>
import { getClients } from '@/services/clients.js';

export default {
  name: 'CamerasPage',
  middleware: 'authenticate',
  data: () => ({
    cameras: [],
    isLoading: true,
  }),
  mounted() {
    this.isLoading = true;

    getClients()
    .then((cameras) => {
      this.cameras = cameras;
      console.log(cameras)
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
</script>

