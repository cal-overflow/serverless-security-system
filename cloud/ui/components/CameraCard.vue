<template>
  <div @mouseover="mouseover = true" @mouseleave="mouseover = false" class="sm:w-4/5 mx-auto flex flex-wrap sm:flex-none bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-full h-auto fill-primary-light dark:fill-primary-dark">
      <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
      <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
    </svg>
    <div class="w-full">
      <div class="flex sm:flex-none justify-between w-full">
        <p class="text-2xl font-bold">
          {{camera.name}}
        </p>
        <button v-if="canEdit" @click.prevent="edit" class="py-1 px-2 hover:text-primary-light dark:hover:text-primary-dark transition duration-500 rounded-full">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />
          </svg>
        </button>
      </div>
      <div class="text-md">
      <p><span class="font-bold">ID:</span> {{camera.id}}</p>
      <p><span class="font-bold">Motion Threshold:</span> {{camera.motion_threshold}}</p>
      <p class="font-bold">Last upload:</p>
        <nuxt-link :to="last_upload_url" class="cursor-pointer hover:underline text-primary-light dark:text-primary-dark">
          {{last_upload_time_formatted}}
        </nuxt-link>
      </div>
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
    },
    canEdit: {
      type: Boolean,
      default: false
    },
  },
  methods: {
    edit() {
      this.$emit('edit');
    }
  },
  computed: {
    last_upload_time_formatted() {
      const dateObj = new Date(parseFloat(this.camera.last_upload_time) * 1000);
      return dateObj.toLocaleString();
    },
    last_upload_url() {
      const keySplitByForwardSlashes = this.camera.last_upload_key.split("/");
      const footageType = keySplitByForwardSlashes[1];
      const uploadDatePath = `${keySplitByForwardSlashes[2]}-${keySplitByForwardSlashes[3]}`;

      const metadata = keySplitByForwardSlashes[4].split("_");
      const uploadTime = metadata[0];
      const clientId = metadata[1].split(".")[0];
      return `footage/${footageType}/${uploadDatePath}?time=${uploadTime}&camera=${clientId}`;
    }
  }
}
</script>

