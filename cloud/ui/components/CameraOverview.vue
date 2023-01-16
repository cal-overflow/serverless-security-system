<template>
  <div class="max-w-screen-sm mx-auto my-6 w-full bg-card-light dark:bg-card-dark p-4 flex flex-wrap shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <div>
      <p class="text-xl font-bold">Cameras</p>

      <div
        v-for="camera in cameras"
        :key="camera.id"
        class="w-full my-4"
      >
        <p class="text-lg font-bold">{{camera.name}}</p>
        <p>
          <span class="text-sm font-bold">Last upload:</span>
          {{camera.last_upload_time_formatted}}
        </p>
      </div>
      
    </div>
  </div>
</template>


<script>
import { getClients } from '@/services/clients.js';

export default {
  name: 'camera-overview',
  data: () => ({
    cameras: [],
  }),
  fetch() {

    getClients(this.videoType, this.options)
    .then((clients) => {
        clients.forEach((client) => {
          const dateObj = new Date(parseFloat(client.last_upload_time) * 1000);
          client.last_upload_time_formatted = dateObj.toLocaleString();
        });
      this.cameras = clients;
    })
    .catch((err) => {
      // TODO - implement error handling
      console.log(err);
    });
  }
}
</script>
