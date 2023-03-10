<template>
  <grid-card
    class="w-full mx-auto 
           px-0 py-0 sm:px-0 sm:py-0 md:p-4
           border border-solid border-primary-light dark:border-primary-dark md:border-none"
  >
    <video
      id="videoPlayer1"
      controls
      class="w-full mx-auto"
      muted
      autoplay
    >
    </video>
    <video
      id="videoPlayer2"
      controls
      class="w-full mx-auto hidden"
      muted
      autoplay
    ></video>
  </grid-card>
</template>

<script>
export default {
  name: 'video-feed-card',
  props: {
    video: {
      type: Object,
      required: true,
    },
    camera: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    nextVideoPlayerIDNumber: 2,
    isLoading: true,
    isUnmounted: false,
    playbackSpeed: 1.0,
    shareableUrl: undefined
  }),
  watch: {
    video(newVideo, oldVideo) {
      const newVideoPlayer = document.getElementById(`videoPlayer${this.nextVideoPlayerIDNumber}`);
      newVideoPlayer.src = newVideo.video_url;
      newVideoPlayer.load();

      newVideoPlayer.oncanplay = () => {

        newVideoPlayer.classList.remove('hidden');
        newVideoPlayer.playbackRate = this.playbackSpeed;

        const otherVideoPlayerIDNumber = this.nextVideoPlayerIDNumber === 1 ? 2 : 1;
        const otherVideoPlayer = document.getElementById(`videoPlayer${otherVideoPlayerIDNumber}`);
        otherVideoPlayer.pause();
        otherVideoPlayer.classList.add('hidden');

        this.nextVideoPlayerIDNumber = otherVideoPlayerIDNumber;
      }
    },
  },
  mounted() {
    const videoPlayer1 = document.getElementById('videoPlayer1');
    const videoPlayer2 = document.getElementById('videoPlayer2');

    videoPlayer1.src = this.video.video_url;
    videoPlayer1.load();


    const videoPlaybackElementOnRateChangeEventHandler = (event) => {
      this.playbackSpeed = event.target.playbackRate;
    };

    const videoPlaybackElementOnEndedEventHandler = () => this.$emit('video-end');

    videoPlayer1.onratechange = videoPlaybackElementOnRateChangeEventHandler;
    videoPlayer1.onended = videoPlaybackElementOnEndedEventHandler;
    videoPlayer2.onratechange = videoPlaybackElementOnRateChangeEventHandler;
    videoPlayer2.onended = videoPlaybackElementOnEndedEventHandler;
  },
  beforeDestroy() {
    this.isUnmounted = true;
  },
  methods: {
    next() {
      this.updateCurrentVideo(this.currentVideoIndex + 1);
    },
    prev() {
      this.updateCurrentVideo(this.currentVideoIndex - 1);
    },
  },
};
</script>

