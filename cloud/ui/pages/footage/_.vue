<template>
  <div class="max-w-screen-lg mx-auto">
    <div class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
      <div class="md:flex align-center justify-between text-center md:text-left">
        <p class="text-4xl font-bold">
          Footage
        </p>
      </div>
      <div class="overflow-x-auto -mr-4">
        <div class="min-w-max flex align-center justify-start gap-4">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 my-auto">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" />
          </svg>
          <label htmlFor="dateInput" class="relative flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="z-10 pointer-events-none w-8 h-8 absolute top-1/2 transform -translate-y-1/2 left-3">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5m-9-6h.008v.008H12v-.008zM12 15h.008v.008H12V15zm0 2.25h.008v.008H12v-.008zM9.75 15h.008v.008H9.75V15zm0 2.25h.008v.008H9.75v-.008zM7.5 15h.008v.008H7.5V15zm0 2.25h.008v.008H7.5v-.008zm6.75-4.5h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V15zm0 2.25h.008v.008h-.008v-.008zm2.25-4.5h.008v.008H16.5v-.008zm0 2.25h.008v.008H16.5V15z" />
            </svg>
            <input
              id="dateInput"
              v-model="dateFilter"
              type="date"
              name="date"
              class="appearance-none resize-none pl-14 pr-6 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            />
          </label>
          <label htmlFor="footageType" class="relative flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="pointer-events-none w-8 h-8 absolute top-1/2 transform -translate-y-1/2 left-3">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.098 19.902a3.75 3.75 0 005.304 0l6.401-6.402M6.75 21A3.75 3.75 0 013 17.25V4.125C3 3.504 3.504 3 4.125 3h5.25c.621 0 1.125.504 1.125 1.125v4.072M6.75 21a3.75 3.75 0 003.75-3.75V8.197M6.75 21h13.125c.621 0 1.125-.504 1.125-1.125v-5.25c0-.621-.504-1.125-1.125-1.125h-4.072M10.5 8.197l2.88-2.88c.438-.439 1.15-.439 1.59 0l3.712 3.713c.44.44.44 1.152 0 1.59l-2.879 2.88M6.75 17.25h.008v.008H6.75v-.008z" />
            </svg>
            <select
              v-model="footageType"
              name="footageType"
              class="appearance-none resize-none pl-14 pr-6 py-2.5 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            >
              <option value="all">All footage</option>
              <option value="activity">With activity</option>
              <option value="normal">Without activity</option>
            </select>
          </label>
          <label htmlFor="cameraFilter" class="relative flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="pointer-events-none w-8 h-8 absolute top-1/2 transform -translate-y-1/2 left-3">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
            </svg>
            <select
              v-model="cameraFilter"
              name="cameraFilter"
              class="appearance-none resize-none pl-14 pr-6 py-2.5 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            >
              <option value="">Any Camera</option>
              <option v-for="camera in cameras" :key="camera.id" :value="camera.id">{{camera.name}}</option>
            </select>
          </label>

          <button
            :disabled="!hasChanges"
            :class="`rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white transition duration-1000 ${hasChanges ? 'opacity-1 cursor-pointer' : 'opacity-25 cursor-default'}`"
            @click="applyChanges"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
            Apply filter
          </button>
        </div>
      </div>
    </div>

    <!-- Change the ordering of these components on small screens -->
    <div
      v-if="filteredVideos.length"
      class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 md:p-0
             md:bg-main-light md:dark:bg-main-dark grid md:grid-cols-6 justify-center sm:justify-between gap-4 md:gap-10
             motion-safe:animate-fade-in-fast transition"
    >

      <video-feed-card 
        :video="selectedVideo"
        :camera="selectedVideoCamera"
        class="md:col-span-4"
        @video-end="next"
      />

      <grid-card class="block md:hidden w-full md:col-span-2 flex-col">
        <div class="w-full flex justify-between items-center">
          <p class="font-bold">Current video</p>
          <label htmlFor="timePicker" class="relative flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="z-10 pointer-events-none w-8 h-8 absolute top-1/2 transform -translate-y-1/2 left-3">
  <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <select
              v-model="selectedVideoIndex"
              name="selectedVideoIndex"
              required
              class="appearance-none resize-none pl-14 pr-6 py-2 mx-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
            >
              <option
                v-for="(video, i) in filteredVideos"
                :key="`video-${video.time}-link`"
                :value="i"
              >
                {{video.time_formatted}}
              </option>
            </select>
          </label>
        </div>
      </grid-card>

      <grid-card class="hidden md:block md:col-span-2 flex-col">
        <p class="font-bold">Videos</p>
        <div class="max-h-96 overflow-y-scroll">
          <p
            v-for="(video, i) in filteredVideos"
            :key="`video-${video.time}-link`"
            :class="`cursor-pointer hover:underline ${selectedVideoIndex === i ? 'font-bold text-primary-light dark:text-primary-dark' : ''}`"
            @click="updateCurrentVideo(i)"
          >
            {{video.time_formatted}}
          </p>
        </div>
      </grid-card>

      <video-metadata-card :video="selectedVideo" :camera="selectedVideoCamera" :date-filter="dateFilter" @share="share" />
    </div>
    <div
      v-else
      class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 md:p-0
             md:bg-main-light md:dark:bg-main-dark grid grid-cols-1 justify-center sm:justify-between gap-4 md:gap-10
             motion-safe:animate-fade-in-fast transition"
    >
      <grid-card>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
        </svg>
        <p>
          <span class="text-lg font-bold">No videos found</span>
          <br />
          Try adjusting the filter
        </p>
      </grid-card>
    </div>
    <alert v-if="shareableUrl" title="URL Copied" @close="shareableUrl = undefined">
      <input
        :value="shareableUrl"
        onclick="this.select();"
        readonly
        class="w-full resize-none px-4 py-2 mb-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
      />
      <p>This shareable URL has been copied to your clipboard.</p>
      <small><strong>Note:</strong> Only users with accounts can access this URL.</small>
    </alert>
  </div>
</template>

<script>
import { getFootage } from '@/services/footage.js';

const validFootageTypes = [ 'all', 'activity', 'normal' ];


export default {
  name: 'IndexPage',
  middleware: 'authenticate',
  async asyncData({ params, route, error }) {
    const lastForwardSlashIndex = params.pathMatch.includes('/') ? params.pathMatch.lastIndexOf('/') : params.pathMatch.length;
    const footageType = params.pathMatch.slice(0, lastForwardSlashIndex);

    if (!validFootageTypes.includes(footageType)) {
      return error({
        statusCode: 404,
        message: 'The requested footage does not exist. Please check the URL.',
        error: new Error(`Footage type "${footageType}" is not one of ${validFootageTypes}.`)
      });
    }

    return await getFootage({ params, route, footageType });
  },
  data: () => ({
    isShowingFilter: false,
    shareableUrl: undefined,
  }),
  computed: {
    hasChanges() {
      return this.originalFilter.dateFilter !== this.dateFilter || this.originalFilter.cameraFilter !== this.cameraFilter || this.originalFilter.footageType !== this.footageType;
    },
  },
  watch: {
    selectedVideoIndex(newIndex) {
      this.updateCurrentVideo(newIndex);
    },
  },
  methods: {
    updateCurrentVideo(index) {
      if (index < 0 || this.filteredVideos.length <= index) return;
      this.selectedVideo = this.filteredVideos[index];
      this.selectedVideoIndex = index;
    },
    share() {
      this.shareableUrl = `https://${window.location.hostname}/footage/${this.footageType}/${this.dateFilter}?time=${this.selectedVideo.time}&camera=${this.selectedVideoCamera.id}`;
      navigator.clipboard.writeText(this.shareableUrl);
    },
    prev() {
      this.updateCurrentVideo(this.selectedVideoIndex - 1);
    },
    next() {
      this.updateCurrentVideo(this.selectedVideoIndex + 1);
    },
    applyChanges() {
      const originalFilterWithoutCamera = {
        dateFilter: this.originalFilter.dateFilter,
        footageType: this.originalFilter.footageType,
      };
      const currentFilterWithoutCamera = {
        dateFilter: this.dateFilter,
        footageType: this.footageType,
      };
      const isNonCameraFilterUnchanged = JSON.stringify(originalFilterWithoutCamera) === JSON.stringify(currentFilterWithoutCamera);

      if (this.cameraFilter !== this.originalFilter.cameraFilter && isNonCameraFilterUnchanged) {
        // don't redirect if the change is ONLY the camera filter
        if (!this.cameraFilter) {
          this.filteredVideos = this.videos;
        }
        else this.filteredVideos = this.videos.filter(({ camera }) => camera === this.cameraFilter);
        this.originalFilter.cameraFilter = this.cameraFilter;
        return;
      }

      const queryParams = this.cameraFilter ? `?camera=${this.cameraFilter}` : '';
      this.$router.push(`/footage/${this.footageType}/${this.dateFilter}${queryParams}`);
    }
  },
};
</script>

