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

      <div class="w-full flex items-center justify-between">

        <div>
          <button @click="prev">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
          </button>
          <button @click="isFilterVisible = !isFilterVisible" title="Toggle filter" class="p-2 mt-2 mb-4 ">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" :class="`w-8 h-8 transition ${isFilterVisible ? 'hidden' : ''}`">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-9.75 0h9.75" />
            </svg>

            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"  :class="`w-8 h-8 transition ${isFilterVisible ? '' : 'hidden'}`">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div v-if="isFilterVisible">
          <button
            :class="`rounded-full p-2 mt-2 mb-4 transition ${currentFilterOption === 'footage' ? 'bg-primary-light dark:bg-primary-dark text-white' : ''}`"
            @click="currentFilterOption = 'footage'"
            title="Footage type"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 01-1.125-1.125M3.375 19.5h1.5C5.496 19.5 6 18.996 6 18.375m-3.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-1.5A1.125 1.125 0 0118 18.375M20.625 4.5H3.375m17.25 0c.621 0 1.125.504 1.125 1.125M20.625 4.5h-1.5C18.504 4.5 18 5.004 18 5.625m3.75 0v1.5c0 .621-.504 1.125-1.125 1.125M3.375 4.5c-.621 0-1.125.504-1.125 1.125M3.375 4.5h1.5C5.496 4.5 6 5.004 6 5.625m-3.75 0v1.5c0 .621.504 1.125 1.125 1.125m0 0h1.5m-1.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m1.5-3.75C5.496 8.25 6 7.746 6 7.125v-1.5M4.875 8.25C5.496 8.25 6 8.754 6 9.375v1.5m0-5.25v5.25m0-5.25C6 5.004 6.504 4.5 7.125 4.5h9.75c.621 0 1.125.504 1.125 1.125m1.125 2.625h1.5m-1.5 0A1.125 1.125 0 0118 7.125v-1.5m1.125 2.625c-.621 0-1.125.504-1.125 1.125v1.5m2.625-2.625c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125M18 5.625v5.25M7.125 12h9.75m-9.75 0A1.125 1.125 0 016 10.875M7.125 12C6.504 12 6 12.504 6 13.125m0-2.25C6 11.496 5.496 12 4.875 12M18 10.875c0 .621-.504 1.125-1.125 1.125M18 10.875c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125m-12 5.25v-5.25m0 5.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125m-12 0v-1.5c0-.621-.504-1.125-1.125-1.125M18 18.375v-5.25m0 5.25v-1.5c0-.621.504-1.125 1.125-1.125M18 13.125v1.5c0 .621.504 1.125 1.125 1.125M18 13.125c0-.621.504-1.125 1.125-1.125M6 13.125v1.5c0 .621-.504 1.125-1.125 1.125M6 13.125C6 12.504 5.496 12 4.875 12m-1.5 0h1.5m-1.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125M19.125 12h1.5m0 0c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h1.5m14.25 0h1.5" />
            </svg>
          </button>
          <button
            :class="`rounded-full p-2 mt-2 mb-4 transition ${currentFilterOption === 'camera' ? 'bg-primary-light dark:bg-primary-dark text-white' : ''}`"
            @click="currentFilterOption = 'camera'"
            title="Camera"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
            </svg>
          </button>
          <button
            :class="`rounded-full p-2 mt-2 mb-4 transition ${currentFilterOption === 'date' ? 'bg-primary-light dark:bg-primary-dark text-white' : ''}`"
            @click="currentFilterOption = 'date'"
            title="Date"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5m-9-6h.008v.008H12v-.008zM12 15h.008v.008H12V15zm0 2.25h.008v.008H12v-.008zM9.75 15h.008v.008H9.75V15zm0 2.25h.008v.008H9.75v-.008zM7.5 15h.008v.008H7.5V15zm0 2.25h.008v.008H7.5v-.008zm6.75-4.5h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V15zm0 2.25h.008v.008h-.008v-.008zm2.25-4.5h.008v.008H16.5v-.008zm0 2.25h.008v.008H16.5V15z" />
            </svg>
          </button>
        </div>
        <p v-else-if="currentVideoMetadata">
          {{currentVideoMetadata}}
        </p>

        <div>
          <button
            v-if="isFilterVisible"
            @click="applyFilter"
            :disabled="!(isChanges && isDateValid)"
            title="Apply"
            :class="isChanges && isDateValid ? 'cursor-pointer' : 'cursor-default'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" :class="`w-8 h-8 transition duration-500 ${!(isChanges && isDateValid) ? 'text-extra-gray-dark dark:text-extra-gray-light' : 'text-primary-light dark:text-primary-dark'}`">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" />
            </svg>
          </button>
          <button @click="next">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" :class="`w-8 h-8 ${currentVideoIndex + 1 === videosFilteredByCamera.length ? 'text-extra-gray-dark dark:text-extra-gray-light' : ''}`">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>
          </button>
        </div>
      </div>
      <div>
        <select
          v-model="type"
          name="type"
          :class="`appearance-none w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition ${isFilterVisible && currentFilterOption === 'footage' ? '' : 'hidden'}`"
        >
          <option value="all">All footage</option>
          <option value="motion">With activity</option>
          <option value="motionless">Without activity</option>
        </select>
        <select
          v-model="camera"
          name="camera"
          :class="`appearance-none w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition ${isFilterVisible && currentFilterOption === 'camera' ? '' : 'hidden'}`"
        >
          <option value="">Any Camera</option>
          <option v-for="camera in cameras" :key="camera.id" :value="camera.id">{{camera.name}}</option>
        </select>
        <input
          v-model="dateFilter"
          type="date"
          name="date"
          id="dateInput"
          :class="`appearance-none w-full resize-none px-4 py-2 bg-extra-gray-light dark:bg-extra-gray-dark rounded-lg outline-none focus:rounded-sm focus:ring focus:ring-primary-light dark:focus:ring-primary-dark transition ${isFilterVisible && currentFilterOption === 'date' ? '' : 'hidden'}`"
        />
        <p :class="`text-sm text-extra-gray-dark dark:text-extra-gray-light transition duration-250 ${isDateValid ? 'opacity-0' : 'opacity-1'}`">Invalid date</p>
      </div>
        </div>

       <div class="w-full md:w-1/5 mx-auto pl-4">



      <div class="w-1/2 md:w-full text-lg">
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
    isFilterVisible: false,
    currentFilterOption: 'footage',
    isUnmounted: false,
    currentVideo: undefined,
    currentVideoIndex: 0,
    backgroundPlayerId: 1,
    playbackSpeed: 1.0,
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
        loadingVideoElement.playbackRate = this.playbackSpeed;

        const otherVideoElement = document.getElementById(`video${previousVideoPlayerId}`);
        otherVideoElement.pause();
        otherVideoElement.classList.add('hidden');
      };

      loadingVideoElement.onratechange = (event) => {
        this.playbackSpeed = event.target.playbackRate;
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
        if (this.camera) {
          this.videosFilteredByCamera = this.videos.filter(({ camera }) => camera === this.camera);
        }
        else this.videosFilteredByCamera = this.videos;
        this.updateCurrentVideo(0);
      }
      else this.getVideos();


      this.previousFilter = {
        type: this.type,
        camera: this.camera,
        dateFilter: this.dateFilter,
      };

    },
    next() {
      this.updateCurrentVideo(this.currentVideoIndex + 1);
    },
    prev() {
      this.updateCurrentVideo(this.currentVideoIndex - 1);
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
    },
    currentVideoMetadata() {
      if (!this.videos.length) return;

      const currentVideo = this.videos[this.currentVideoIndex];
      let cameraName = '---';
      if (this.cameras.length) {
        cameraName = this.cameras.find(({ id }) => currentVideo.camera === id).name;
      }
      return `${cameraName} ${currentVideo.time_formatted}`;
    }
  }
}
</script>

