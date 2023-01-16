<template>
  <div class="max-w-screen-lg mx-auto bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <div>
      <p class="text-lg font-bold">{{descriptionText}}</p>
    </div>
    <div class="flex flex-wrap md:flex-nowrap">
      <div v-if="isLoading">
        TODO - Add a loading indicator here
      </div>

      <div>
      </div>

      <div class="w-full md:w-4/5 mx-auto items-start">
        <video
          controls
          id="video1"
          class="w-full mx-auto"
          muted
          autoplay
        ></video>
        <video
          controls
          id="video2"
          class="w-full mx-auto hidden"
          muted
          autoplay
        ></video>
        </div>
       <div class="w-full md:w-1/5 mx-auto pl-4">

        <label for="date" class="font-bold">Date</label>
        <input
          v-model="dateFilter"
          type="string"
          name="date"
          id="dateInput"
          class="w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light focus:dark:ring-primary-dark transition"
        />
       <p class="font-bold">Times</p>
       <div v-if="videos.length > 0" class="max-h-96 overflow-y-scroll">
          <p
            v-for="(video, i) in videos"
            :key="`video-${video.time}-link`"
            :class="`cursor-pointer hover:underline ${currentVideoIndex === i ? 'font-bold text-primary-light dark:text-primary-dark' : ''}`"
            @click="updateCurrentVideo(i)"
          >
            {{video.time_formatted}}
          </p>
        </div>
        <div v-else class="motion-safe:animate-pulse max-h-96 overflow-y-scroll">
          <div v-for="i in 40" :key="`lazy-video-link-${i}`" class="bg-gray-400 w-4/5 h-4 my-2" />
          <div class="h-2" />
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { getVideos } from '@/services/videos.js';

const today = new Date()

export default {
  name: 'video-feed',
  props: {
    type: {
      type: String,
      default: 'all'
    }
  },
  data: () => ({
    videos: [],
    isLoading: true,
    isUnmounted: false,
    currentVideo: undefined,
    currentVideoIndex: 0,
    backgroundPlayerId: 1,
    descriptionText: 'Latest footage',
    dateFilter: `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`
  }),
  mounted() {
    if (this.type !== 'all' && this.type !== 'motion' && this.type !== 'motionless') {
      throw new Error('Invalid type prop provided. Must be all, motion, or motionless'); // TODO - figure out what to actually do here - maybe just default to all?
    }
    
    if (this.type === 'all') {
      this.descriptionText = 'Latest footage';
    }
    else if (this.type === 'motion') {
      this.descriptionText = 'Latest footage with activity';
    }
    else if (this.type === 'motionless') {
      this.descriptionText = 'Latest footage with no activity';
    }
  },
  fetch() {
    this.getVideos();
  },
  beforeDestroy() {
    this.isUnmounted = true;
  },
  methods: {
    getVideos() {
      this.isLoading = true;
      this.videos = [];
      const options = { date: this.dateFilter }

      getVideos(this.type, options)
      .then((videos) => {
          if (this.isUnmounted) {
            return; // this api call can take a while so if the page is unmounted then cancel the remaining logic
          }
        videos.forEach((video) => {
          video.time_formatted = video.time.replace(/-/g, ':');
        });
        this.videos = videos;
        this.updateCurrentVideo(0);
      })
      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
      })
      .finally(() => {
        this.isLoading = false;
      });
    },
    updateCurrentVideo(index) {
      this.currentVideo = this.videos[index];

      console.log('changing video to ', this.currentVideo.time)
      
      const previousVideoPlayerId = this.backgroundPlayerId === 1 ? 2 : 1;

      const loadingVideoElement = document.getElementById(`video${this.backgroundPlayerId}`);
      loadingVideoElement.src = this.currentVideo.video_url;
      loadingVideoElement.load();

      loadingVideoElement.oncanplay = () => {
        this.backgroundPlayerId = this.backgroundPlayerId === 1 ? 2 : 1;
        this.currentVideoIndex = index;
        loadingVideoElement.classList.remove('hidden');

        const otherVideoElement = document.getElementById(`video${previousVideoPlayerId}`);
        otherVideoElement.pause();
        otherVideoElement.classList.add('hidden');
      };

      loadingVideoElement.onended = () => {
        if (index === this.videos.length - 1) {
          return;
        }

        console.log('ENDED', this.currentVideoIndex);
        this.updateCurrentVideo(this.currentVideoIndex + 1);
      };
    },
    isValidDate(dateString) {
      // First check for the pattern
      if (!/^\d{4}-\d{1,2}-\d{1,2}$/.test(dateString))
          return false;

      console.log('made it this far')

      // Parse the date parts to integers
      const parts = dateString.split("-");
      const year = parseInt(parts[0], 10);
      const month = parseInt(parts[1], 10);
      const day = parseInt(parts[2], 10);

      // Check the ranges of month and year
      if (year < 1000 || year > 3000 || month === 0 || month > 12)
          return false;

      const monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];

      // Adjust for leap years
      if (year % 400 === 0 || (year % 100 !== 0 && year % 4 === 0))
          monthLength[1] = 29;

      // Check the range of the day
      return day > 0 && day <= monthLength[month - 1];
    },
  },
  watch: {
    dateFilter(newDate, oldDate) {
      if (this.isValidDate(newDate)) {
        this.getVideos();
      }
      else {
        console.log('Invalid date');
        // TODO - show the user their date is invalid
      }
    }
  }
}
</script>

