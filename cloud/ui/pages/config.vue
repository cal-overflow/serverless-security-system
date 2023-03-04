<template>
  <div class="max-w-screen-lg mx-auto">
    <div class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
      <div class="w-full md:w-2/3 mx-auto">
        <div class="mb-4">
          <p class="text-2xl font-bold">
            Configuration

            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </p>
          <p class="text-md">
            System-wide settings
          </p>
        </div>

        <p v-if="!hasPermissionToEdit" class="font-bold text-md text-primary-light dark:text-primary-dark">
          Only Admin users have permission to update the system configuration.
        </p>

        <form @submit.prevent="saveUpdates">
          <p class="text-xl font-bold">
            Camera
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
            </svg>
          </p>
          <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
            Settings shared by cameras
          </p>
          <div class="md:flex align-center items-center">
            <div class="w-full md:w-1/2">
              <label for="clipLength" class="font-bold text-right">Clip length</label>
            </div>
            <select
              v-model="clipLength"
              name="clipLength"
              required
              :disabled="!hasPermissionToEdit"
              class="appearance-none w-full md:w-1/2 resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            >
              <option value="10">10 seconds</option>
              <option value="15">15 seconds</option>
              <option value="20">20 seconds</option>
              <option value="30">30 seconds</option>
              <option value="60">1 minute</option>
            </select>
          </div>
          <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
            The duration, in seconds, of clips to record.
          </p>
          <br />


          <div class="md:flex align-center items-center">
            <div class="w-full md:w-1/2">
              <label for="clipsPerUpload" class="font-bold text-right">Clips per upload</label>
            </div>
            <select
              v-model="clipsPerUpload"
              name="clipsPerUpload"
              required
              :disabled="!hasPermissionToEdit"
              class="appearance-none w-full md:w-1/2 resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            >
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </div>
          <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
            The number of clips to record before an attempt to upload.
          </p>
          <br />

          <div class="md:flex align-center items-center">
            <div class="w-full md:w-1/2">
              <label for="defaultMotionThreshold" class="font-bold text-right">Default Motion Sensitivity</label>
            </div>
            <select
              v-model="defaultMotionThreshold"
              name="defaultMotionThreshold"
              required
              :disabled="!hasPermissionToEdit"
              class="appearance-none w-full md:w-1/2 resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            >
              <option value="15000">Lowest sensitivity (15000)</option>
              <option value="10000">Low sensitivity (10000)</option>
              <option value="7500">Moderate sensitivity (7500)</option>
              <option value="5000">High sensitivity (5000)</option>
              <option value="2500">Highest sensitivity (2500)</option>
            </select>
          </div>
          <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
            The default sensitivity value for cameras to determine if motion is present in a video. Note that this value is overridden by each camera's motion threshold value.
          </p>
          <br />

          <div class="flex align-center items-center">
            <div class="w-1/2 md:w-1/2">
              <label for="isMotionOutlined" class="font-bold text-right">Outline Motion</label>
            </div>
            <toggle v-model="isMotionOutlined" :showLabel="true" />
          </div>
          <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
            Whether or not motion should be outlined.
          </p>
          <br />


          <p class="text-xl font-bold">
            System

            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H6.75A2.25 2.25 0 004.5 6.75v10.5a2.25 2.25 0 002.25 2.25zm.75-12h9v9h-9v-9z" />
            </svg>
          </p>
          <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
            User-interface and data settings
          </p>

          <div class="md:flex align-center items-center">
            <div class="w-full md:w-1/2">
              <label for="presignUrlExpirationTime" class="font-bold text-right">URL expiration time</label>
            </div>
            <select
              v-model="presignUrlExpirationTime"
              name="presignUrlExpirationTime"
              required
              :disabled="!hasPermissionToEdit"
              class="appearance-none w-full md:w-1/2 resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            >
              <option value=3600>1 hour</option>
              <option value="7200">2 hours</option>
              <option value="14400">4 hours</option>
              <option value="21600">6 hours</option>
              <option value="43200">12 hours</option>
              <option value="86400">24 hours</option>
              <option value="172800">2 days</option>
              <option value="259200">3 days</option>
              <option value="604800">1 week</option>
            </select>
          </div>
          <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
            How long video URLs should be valid for when given to a signed in user. Note that the user can simply refresh their page if their URL expires.
          </p>
          <br />


          <div class="md:flex align-center items-center">
            <div class="w-full md:w-1/2">
              <label for="daysToKeepMotionlessVideos" class="font-bold text-right">Keep motionless videos</label>
            </div>
            <select
              v-model="daysToKeepMotionlessVideos"
              name="daysToKeepMotionlessVideos"
              required
              :disabled="!hasPermissionToEdit"
              class="appearance-none w-full md:w-1/2 resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            >
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
            How long videos without motion should be kept. Note: Videos with motion are kept forever.
          </p>

          <div class="flex justify-between w-full">
            <p class="text-sm my-auto">{{infoMessage}}</p>
            <input
              type="submit"
              value="Save"
              :disabled="!hasPermissionToEdit"
              :class="`rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white transition duration-1000 ${hasPermissionToEdit ? 'opacity-1 cursor-pointer' : 'opacity-25 cursor-default'}`"
            />
          </div>

        </form>
      </div>
    </div>
  </div>
</template>


<script>
import { getConfig, updateConfig } from '@/services/config.js';

export default {
  name: 'ConfigPage',
  middleware: 'authenticate',
  async asyncData({ user }) {
    const config = await getConfig()
      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
      });

    return {
      hasPermissionToEdit: user.admin,
      clipLength: config.clip_length,
      clipsPerUpload: config.clips_per_upload,
      presignUrlExpirationTime: config.presign_url_expiration_time,
      defaultMotionThreshold: config.default_motion_threshold,
      daysToKeepMotionlessVideos: config.days_to_keep_motionless_videos,
      isMotionOutlined: config.is_motion_outlined,
    }
  },
  data: () => ({
    infoMessage: ''
  }),
  methods: {
    saveUpdates() {
      if (!this.hasPermissionToEdit) return;

      this.infoMessage = 'Saving...';

      updateConfig({
        clip_length: parseInt(this.clipLength),
        clips_per_upload: parseInt(this.clipsPerUpload),
        presign_url_expiration_time: parseInt(this.presignUrlExpirationTime),
        default_motion_threshold: parseInt(this.defaultMotionThreshold),
        days_to_keep_motionless_videos: parseInt(this.daysToKeepMotionlessVideos),
        is_motion_outlined: this.isMotionOutlined,
      })
      .then(() => {
        this.infoMessage = 'Changes successfully saved';
      })
      .catch((err) => {
        this.infoMessage = err.message || 'An error occurred';
      });
    } 
  }
}
</script>

