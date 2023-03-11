<template>
  <grid-card>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="w-2/3 mx-auto h-auto fill-primary-light dark:fill-primary-dark"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"
      />
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z"
      />
    </svg>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="w-10 h-10 absolute z-10 text-primary-light dark:text-primary-dark motion-safe:animate-fade-in"
    >
      <path
        v-if="!camera.is_active"
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"
      />
      <path
        v-else-if="isHealthy"
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M8.288 15.038a5.25 5.25 0 017.424 0M5.106 11.856c3.807-3.808 9.98-3.808 13.788 0M1.924 8.674c5.565-5.565 14.587-5.565 20.152 0M12.53 18.22l-.53.53-.53-.53a.75.75 0 011.06 0z"
      />
      <path
        v-else
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
      />
    </svg>
    <div class="w-full">
      <div class="flex sm:flex-none justify-between w-full">
        <p class="text-2xl font-bold">
          {{ camera.name }}
        </p>
        <button
          v-if="canEdit"
          class="py-1 px-2 hover:text-primary-light dark:hover:text-primary-dark transition duration-500 rounded-full"
          @click.prevent="edit"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125"
            />
          </svg>
        </button>
      </div>
      <div class="text-md">
        <p><span class="font-bold">ID:</span> {{ camera.id }}</p>
        <p>
          <span class="font-bold">Motion Threshold:</span>
          {{ camera.motion_threshold }}
        </p>
        <p class="font-bold">Last upload:</p>
        <nuxt-link
          :to="last_upload_url"
          class="cursor-pointer hover:underline text-primary-light dark:text-primary-dark"
        >
          {{ last_upload_time_formatted }}
        </nuxt-link>
      </div>
    </div>
  </grid-card>
</template>

<script>
export default {
  name: 'CameraCard',
  props: {
    camera: {
      type: Object,
      required: true,
    },
    canEdit: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    isHealthy() {
      const now = new Date().getTime();
      const lastUpload = new Date(
        parseFloat(this.camera.last_upload_time) * 1000
      ).getTime();

      // If more than half an hour has passed since the last upload time
      if (lastUpload + 30 * 60 * 1000 < now) {
        return false;
      }

      return true;
    },
    last_upload_time_formatted() {
      const dateObj = new Date(parseFloat(this.camera.last_upload_time) * 1000);
      return dateObj.toLocaleString();
    },
    last_upload_url() {
      const keySplitByForwardSlashes = this.camera.last_upload_key.split('/');
      const footageType = keySplitByForwardSlashes[1];
      const uploadDatePath = `${keySplitByForwardSlashes[2]}-${keySplitByForwardSlashes[3]}`;

      const metadata = keySplitByForwardSlashes[4].split('_');
      const uploadTime = metadata[0];
      const clientId = metadata[1].split('.')[0];
      return `footage/${footageType}/${uploadDatePath}?time=${uploadTime}&camera=${clientId}`;
    },
  },
  methods: {
    edit() {
      this.$emit('edit');
    },
  },
};
</script>
