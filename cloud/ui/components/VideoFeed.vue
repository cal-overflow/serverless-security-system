<template>
  <div class="max-w-screen-lg mx-auto bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <div>
      <p class="text-lg font-bold">{{descriptionText}}</p>
    </div>
    <div class="flex flex-wrap md:flex-nowrap">
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


      <div>
        <label for="type" class="font-bold">Type</label>
        <select
          v-model="type"
          name="type"
          class="appearance-none w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
        >
          <option value="all">All footage</option>
          <option value="motion">With activity</option>
          <option value="motionless">Without activity</option>
        </select>
        <br />
        <label for="camera" class="font-bold">Camera</label>
        <select
          v-model="camera"
          name="camera"
          class="appearance-none w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
        >
          <option value="">Any Camera</option>
          <option v-for="camera in cameras" :key="camera.id" :value="camera.id">{{camera.name}}</option>
        </select>
        <br />
        <label for="date" class="font-bold">Date</label>
        <input
          v-model="dateFilter"
          type="date"
          name="date"
          id="dateInput"
          class="appearance-none w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition"
        />
        <p :class="`text-sm text-extra-gray-dark dark:text-extra-gray-light transition duration-250 ${isDateValid ? 'opacity-0' : 'opacity-1'}`">Invalid date</p>
        <button
          :class="`rounded-md py-1 px-2 mt-2 mb-4 bg-primary-light dark:bg-primary-dark text-white transition duration-1000 ${isChanges && isDateValid ? 'opacity-1 cursor-pointer' : 'opacity-25 cursor-default'}`"
          :disabled="!(isChanges && isDateValid)"
          @click="applyFilter"
        >
          Apply Filter
        </button>
      </div>

      <div class="w-1/2 md:w-full mx-auto text-center md:text-left">
        <p class="font-bold">Times</p>
        <div v-if="videosFilteredByCamera.length > 0" class="max-h-96 overflow-y-scroll">
          <p
            v-for="(video, i) in videosFilteredByCamera"
            :key="`video-${video.time}-link`"
            :class="`cursor-pointer hover:underline ${currentVideoIndex === i ? 'font-bold text-primary-light dark:text-primary-dark' : ''}`"
            @click="updateCurrentVideo(i)"
          >
            {{video.time_formatted}}
          </p>
          </div>
          <div v-else-if="isLoading" class="motion-safe:animate-pulse">
            <p>Loading...</p>
          </div>
          <p v-else class="font-bold">No videos found</p>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { getVideos } from '@/services/videos.js';
import { getClients } from '@/services/clients.js';

const formatNumber = (num) => {
  return num.toLocaleString('en-US', {
    minimumIntegerDigits: 2,
    useGrouping: false
  });
};


const today = new Date();
const initialDateFilter = `${today.getFullYear()}-${formatNumber(today.getMonth() + 1)}-${formatNumber(today.getDate())}`


export default {
  name: 'video-feed',
  props: {
    descriptionText: {
      type: String,
      default: 'Latest footage',
    },
  },
  data: () => ({
    times: [
      '0-8',
      '9-16',
      '17-23',
    ],
    videos: [],
    videosFilteredByCamera: [],
    cameras: [],
    isLoading: true,
    isUnmounted: false,
    currentVideo: undefined,
    currentVideoIndex: 0,
    backgroundPlayerId: 1,
    type: 'motion',
    camera: '',
    dateFilter: initialDateFilter,
    previousFilter: {
      type: 'motion',
      camera: '',
      dateFilter: initialDateFilter,
    }
  }),
  fetch() {
    this.getVideos();
    this.getCameras();
  },
  beforeDestroy() {
    this.isUnmounted = true;
  },
  methods: {
    getVideos() {
      this.isLoading = true;
      this.videos = [];
      this.videosFilteredByCamera = [];
      const options = { date: this.dateFilter };

      const fetchVideosTasks = [];

      for (const time of this.times) {
        fetchVideosTasks.push(getVideos(this.type, { ...options, hours: time }));
      }

      Promise.all(fetchVideosTasks).then((videos) => {
        if (this.isUnmounted) {
          return; // this api call can take a while so if the page is unmounted then cancel the remaining logic
        }

        const allVideos = videos.flat();
        console.log(allVideos);

        allVideos.forEach((video) => {
          console.log('video includes time attribute? ', Boolean(video.time));
          video.time_formatted = video.time.replace(/-/g, ':');
        });
        this.videos = allVideos;
        console.log(this.videos);

        if (this.camera) {
          this.videosFilteredByCamera = this.videos.filter(({ camera }) => camera === this.camera);
        }
        else this.videosFilteredByCamera = this.videos;


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
    getCameras() {
      getClients(this.videoType, this.options)
      .then((clients) => {
          clients.forEach((client) => {
            const dateObj = new Date(parseFloat(client.last_upload_time) * 1000);
            client.last_upload_time_formatted = dateObj.toLocaleString();
          });
        this.cameras = clients;
      })
      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
      });
    },
    updateCurrentVideo(index) {
      this.currentVideo = this.videosFilteredByCamera[index];
      if (!this.currentVideo) return;

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
        if (index === this.videosFilteredByCamera.length - 1) {
          return;
        }

        console.log('ENDED', this.currentVideoIndex);
        this.updateCurrentVideo(this.currentVideoIndex + 1);
      };
    },
    applyFilter() {
      if (this.previousFilter.type === this.type && this.previousFilter.dateFilter === this.dateFilter) {
        this.videosFilteredByCamera = this.videos.filter(({ camera }) => camera === this.camera);
      }
      else this.getVideos();


      this.previousFilter = {
        type: this.type,
        camera: this.camera,
        dateFilter: this.dateFilter,
      };

    }
  },
  computed: {
    isDateValid() {
      const dateString = this.dateFilter;
      // First check for the pattern
      if (!/^\d{4}-\d{1,2}-\d{1,2}$/.test(dateString))
          return false;


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
    isChanges() {
      return !(this.previousFilter.type === this.type && this.previousFilter.camera === this.camera && this.previousFilter.dateFilter === this.dateFilter);
    }
  }
}
</script>

