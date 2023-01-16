<template>
  <div class="max-w-screen-lg mx-auto bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <div>
      <p class="text-xl font-bold">{{camera.name}}</p>
      <p class="text-md"><span class="font-bold">ID:</span> {{camera.id}}</p>
      <p class="text-md"><span class="font-bold">Motion Threshold:</span> {{camera.motion_threshold}}</p>
      <p class="text-md">
        <span class="font-bold">Last upload:</span>
        <nuxt-link :to="`/videos/${camera.last_upload_key}`" class="cursor-pointer hover:underline text-primary-light dark:text-primary-dark">
          {{last_upload_time_formatted}}
        </nuxt-link>
      </p>
    </div>
  </div>
</template>


<script>
export default {
  name: 'camera-card',
  props: {
    camera: {
      type: Object,
      required: true
    }
  },
  computed: {
    last_upload_time_formatted() {
      const dateObj = new Date(parseFloat(this.camera.last_upload_time) * 1000);
      return dateObj.toLocaleString();
    }
  }
}
</script>

