<template>
  <div class="max-w-screen-lg mx-auto">
    <div class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
      <p class="text-4xl font-bold text-center md:text-left">
        Settings
      </p>
    </div>
    <form @submit.prevent="saveUpdates">
      <div class="bg-card-light dark:bg-card-dark m-0 md:m-6 pb-8 md:pb-4 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
        <div class="w-full md:w-2/3 mx-auto">
          <div class="text-center md:text-left mb-8">
            <p class="text-xl font-bold">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-12 md:w-8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
              </svg>
              <br class="block md:hidden" />
              Camera
            </p>
            <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
              Settings shared by cameras
            </p>
          </div>
          <div class="md:flex align-center items-center">
            <div class="w-full md:w-1/2">
              <label for="clipLength" class="font-bold text-right">Clip length</label>
            </div>
            <select
              v-if="updatedConfig"
              v-model="updatedConfig.clipLength"
              name="clipLength"
              required
              :disabled="!hasPermissionToEdit"
              class="appearance-none w-full md:w-1/2 resize-none px-4 py-2 my-1 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            >
              <option value="10">10 seconds</option>
              <option value="15">15 seconds</option>
              <option value="20">20 seconds</option>
              <option value="30">30 seconds</option>
              <option value="60">1 minute</option>
            </select>
          </div>
          <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
            The duration of footage clips
          </p>
          <br />


          <div class="md:flex align-center items-center">
            <div class="w-full md:w-1/2">
              <label for="clipsPerUpload" class="font-bold text-right">Clips per upload</label>
            </div>
            <select
              v-if="updatedConfig"
              v-model="updatedConfig.clipsPerUpload"
              name="clipsPerUpload"
              required
              :disabled="!hasPermissionToEdit"
              class="appearance-none w-full md:w-1/2 resize-none px-4 py-2 my-1 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            >
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </div>
          <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
            The number of clips to record per upload
          </p>
          <br />

          <div class="md:flex align-center items-center">
            <div class="w-full md:w-1/2">
              <label for="defaultMotionThreshold" class="font-bold text-right">Default Motion Sensitivity</label>
            </div>
            <select
              v-if="updatedConfig"
              v-model="updatedConfig.defaultMotionThreshold"
              name="defaultMotionThreshold"
              required
              :disabled="!hasPermissionToEdit"
              class="appearance-none w-full md:w-1/2 resize-none px-4 py-2 my-1 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            >
              <option value="15000">Lowest sensitivity (15000)</option>
              <option value="10000">Low sensitivity (10000)</option>
              <option value="7500">Moderate sensitivity (7500)</option>
              <option value="5000">High sensitivity (5000)</option>
              <option value="2500">Highest sensitivity (2500)</option>
            </select>
          </div>
          <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
            The <em>default</em> camera sensitivity
          </p>
          <br />

          <div class="flex align-center items-center">
            <div class="w-1/2 md:w-1/2">
              <label for="isMotionOutlined" class="font-bold text-right">Outline Motion</label>
            </div>
            <toggle v-model="updatedConfig.isMotionOutlined" :showLabel="true" />
          </div>
        </div>
      </div>
      <div class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
        <div class="w-full md:w-2/3 mx-auto">
          <div class="text-center md:text-left mb-8">
            <p class="text-xl font-bold">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-12 md:w-8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H6.75A2.25 2.25 0 004.5 6.75v10.5a2.25 2.25 0 002.25 2.25zm.75-12h9v9h-9v-9z" />
              </svg>
              <br class="block md:hidden" />
              System
            </p>
            <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
              User-interface and data settings
            </p>
          </div>

            <div class="md:flex align-center items-center">
              <div class="w-full md:w-1/2">
                <label for="presignUrlExpirationTime" class="font-bold text-right">Video URL expiration time</label>
              </div>
              <select
                v-if="updatedConfig"
                v-model="updatedConfig.presignUrlExpirationTime"
                name="presignUrlExpirationTime"
                required
                :disabled="!hasPermissionToEdit"
                class="appearance-none w-full md:w-1/2 resize-none px-4 py-2 my-1 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
              >
                <option value=3600>1 hour</option>
                <option value="7200">2 hours</option>
                <option value="14400">4 hours</option>
                <option value="21600">6 hours</option>
                <option value="43200">12 hours</option>
                <option value="86400">24 hours</option>
              </select>
            </div>
            <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
              How long video URLs remain valid
              <br />
              <small>Refreshing the page will generate new URLs</small>
            </p>
            <br />


            <div class="md:flex align-center items-center">
              <div class="w-full md:w-1/2">
                <label for="daysToKeepMotionlessVideos" class="font-bold text-right">Keep motionless videos</label>
              </div>
              <select
                v-if="updatedConfig"
                v-model="updatedConfig.daysToKeepMotionlessVideos"
                name="daysToKeepMotionlessVideos"
                required
                :disabled="!hasPermissionToEdit"
                class="appearance-none w-full md:w-1/2 resize-none px-4 py-2 my-1 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
              >
                <option value="0">Don't keep motionless videos</option>
                <option value="1">1 day</option>
                <option value="2">2 days</option>
                <option value="3">3 days</option>
                <option value="4">4 days</option>
                <option value="4">5 days</option>
                <option value="7">1 week</option>
                <option value="14">2 weeks</option>
              </select>
            </div>
            <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
              How long videos without motion should be kept.
              <br />
              <small>Videos with motion are kept forever</small>
            </p>
        </div>
      </div>

      <div class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
        <div class="flex flex-wrap sm:flex-nowrap justify-between w-full">
          <div v-if="!hasPermissionToEdit">
            <p class="text-lg font-bold text-primary-light dark:text-primary-dark">
              Admin permission required
            </p>
            <p class="text-md">
              Only Admin users have permission to update the system configuration.
            </p>
          </div>
          <p v-else class="my-auto text-extra-gray-dark dark:text-extra-gray-light">{{infoMessage ? infoMessage : hasChanges ? 'Changes not saved' : 'No changes'}}</p>
          <input
            type="submit"
            value="Save"
            :disabled="!hasPermissionToEdit || this.infoMessage === 'Saving...'"
            :class="`rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white transition duration-1000 ${hasPermissionToEdit && hasChanges && this.infoMessage !== 'Saving...' ? 'opacity-1 cursor-pointer' : 'opacity-25 cursor-default'}`"
          />
        </div>
      </div>
    </form>
  </div>
</template>


<script>
import { getConfig, updateConfig } from '@/services/config.js';

const mapConfig = (config) => ({
  clipLength: config.clip_length,
  clipsPerUpload: config.clips_per_upload,
  presignUrlExpirationTime: config.presign_url_expiration_time,
  defaultMotionThreshold: config.default_motion_threshold,
  daysToKeepMotionlessVideos: config.days_to_keep_motionless_videos,
  isMotionOutlined: config.is_motion_outlined,
});

export default {
  name: 'ConfigPage',
  middleware: 'authenticate',
  async asyncData({ user }) {
    const config = await getConfig()
      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
      });

    const originalConfig = mapConfig(config);

    return {
      originalConfig,
      updatedConfig: { ...originalConfig },
      hasPermissionToEdit: user.admin,
      infoMessage: 'Configuration synced'
    };
  },
  mounted() {
    window.onbeforeunload = () => {
      if (this.hasChanges) {
        return "Your changes are not saved";
      }
    };
  },
  methods: {
    saveUpdates() {
      if (!this.hasPermissionToEdit || !this.hasChanges || this.infoMessage === 'Saving...') return;

      this.infoMessage = 'Saving...';

      updateConfig({
        clip_length: parseInt(this.updatedConfig.clipLength),
        clips_per_upload: parseInt(this.updatedConfig.clipsPerUpload),
        presign_url_expiration_time: parseInt(this.updatedConfig.presignUrlExpirationTime),
        default_motion_threshold: parseInt(this.updatedConfig.defaultMotionThreshold),
        days_to_keep_motionless_videos: parseInt(this.updatedConfig.daysToKeepMotionlessVideos),
        is_motion_outlined: this.updatedConfig.isMotionOutlined,
      })
      .then(() => {
        this.$nuxt.refresh(); // refresh asyncData
      })
      .catch((err) => {
        this.infoMessage = err.message || 'An error occurred';
      });
    } 
  },
  computed: {
    hasChanges() {
      return JSON.stringify(this.originalConfig) !== JSON.stringify(this.updatedConfig);
    }
  },
}
</script>

