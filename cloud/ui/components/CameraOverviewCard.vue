<template>
  <div
    @mouseover="mouseover = true"
    @mouseleave="mouseover = false"
    class="flex flex-wrap md:flex-none
           bg-card-light dark:bg-card-dark
           p-8 sm:p-4 mx-auto
           sm:w-full md:shadow-lg md:dark:shadow-shadow-dark
           hover:shadow-none hover:rounded
           static
           motion-safe:animate-fade-in-fast transition"
  >
    <div class="text-center md:text-left mb-8 w-full">
      <p class="text-xl font-bold">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="inline w-16 md:w-8 h-auto">
          <path d="M12 9a3.75 3.75 0 100 7.5A3.75 3.75 0 0012 9z" />
          <path fill-rule="evenodd" d="M9.344 3.071a49.52 49.52 0 015.312 0c.967.052 1.83.585 2.332 1.39l.821 1.317c.24.383.645.643 1.11.71.386.054.77.113 1.152.177 1.432.239 2.429 1.493 2.429 2.909V18a3 3 0 01-3 3h-15a3 3 0 01-3-3V9.574c0-1.416.997-2.67 2.429-2.909.382-.064.766-.123 1.151-.178a1.56 1.56 0 001.11-.71l.822-1.315a2.942 2.942 0 012.332-1.39zM6.75 12.75a5.25 5.25 0 1110.5 0 5.25 5.25 0 01-10.5 0zm12-1.5a.75.75 0 100-1.5.75.75 0 000 1.5z" clip-rule="evenodd" />
        </svg>
        <br class="block md:hidden" />
        Cameras
      </p>
    </div>
    <div class="w-full text-center">
      <p class="text-4xl">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-2/5 md:w-1/3 text-primary-light dark:text-primary-dark motion-safe:animate-fade-in">
          <path v-if="healthyCameraCount === activeCameraCount" stroke-linecap="round" stroke-linejoin="round" d="M8.288 15.038a5.25 5.25 0 017.424 0M5.106 11.856c3.807-3.808 9.98-3.808 13.788 0M1.924 8.674c5.565-5.565 14.587-5.565 20.152 0M12.53 18.22l-.53.53-.53-.53a.75.75 0 011.06 0z" />
          <path v-else stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
        </svg>
        <br />
        {{healthyCameraCount === activeCameraCount ? 'Healthy' : 'Unhealthy' }}
      </p>
      <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
        {{healthyCameraCount}} / {{activeCameraCount}}
        online
      </p>
      <div class="text-center my-2">
        <nuxt-link to="/cameras" class="text-primary-light dark:text-primary-dark underline hover:no-underline">
          Dashboard
        </nuxt-link>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'camera-overview-card',
  props: {
    cameras: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    healthyCameraCount: 0,
    activeCameraCount: 0,
  }),
  mounted() {
    let healthyCameraCount = 0;
    let activeCameraCount = 0;

    this.cameras.forEach((camera) => {
      if (this.isHealthy(camera)) {
        healthyCameraCount++;
      }
      if (camera.is_active) {
        activeCameraCount++;
      }
    });

    this.healthyCameraCount = healthyCameraCount;
    this.activeCameraCount = activeCameraCount;
  },
  methods: {
    isHealthy(camera) {
      const now = new Date().getTime()
      const lastUpload = new Date(parseFloat(camera.last_upload_time) * 1000).getTime();

      // If more than half an hour has passed since the last upload time
      if (lastUpload + (30 * 60 * 1000) < now) {
        return false;
      }

      return true;
      
    },
    last_upload_time_formatted(camera) {
      const dateObj = new Date(parseFloat(camera.last_upload_time) * 1000);
      return dateObj.toLocaleString();
    },
  }
}
</script>
