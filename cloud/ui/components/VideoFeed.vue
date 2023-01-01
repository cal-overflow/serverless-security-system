<template>
  <div class="max-w-screen-lg mx-auto bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <div>
      <p class="text-lg font-bold">{{descriptionText}}</p>
    </div>
    <div class="flex flex-wrap md:flex-nowrap">
      <div v-if="isLoading">
        TODO - Add a loading indicator here
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
    currentVideo: undefined,
    currentVideoIndex: 0,
    backgroundPlayerId: 1,
    descriptionText: 'Latest footage',
    options: {
      date: '2022-12-30'
    },
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
    this.isLoading = true;

    getVideos(this.type, this.options)
    .then((videos) => {
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
  methods: {
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


    }
  }
}
</script>

