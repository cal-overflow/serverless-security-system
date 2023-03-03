<template>
  <div class="max-w-screen-lg mx-auto">
    <div class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
      <div class="w-full md:w-2/3 mx-auto">
        <div class="mb-4">
          <p class="text-2xl font-bold">Configuration</p>
          <p class="text-md">
            System-wide settings
          </p>
        </div>

        <p v-if="!hasPermissionToEdit" class="font-bold text-md text-primary-light dark:text-primary-dark">
          Only Admin users have permission to update the system configuration.
        </p>

        <form @submit.prevent="saveUpdates">
          <p class="text-xl font-bold">Camera</p>
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


          <p class="text-xl font-bold">System</p>
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

