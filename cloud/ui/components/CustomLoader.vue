<template>
  <div :class="`pointer-events-none	
                z-50 w-screen h-screen flex fixed top-0 left-0 p-0 m-0
                bg-card-light dark:bg-card-dark
                flex align-center
                motion-safe:animate-fade-in-fast transition duration-500
                ${loading ? 'opacity-100' : 'opacity-0'}
              `"
  >
    <p class="w-full text-primary-light dark:text-primary-dark text-sm text-center my-auto">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" :class="`w-1/4 max-w-lg h-auto mx-auto transition ease-in-out delay-750 duration-1000 ${loading ? 'opacity-100' : 'opacity-0'} inline`">
        <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd" class="loader" />
      </svg>
      <br />
      <span :class="`text-extra-gray-dark dark:text-extra-gray-light transition ease-in-out delay-1000 duration-1000 ${loading ? 'opacity-100' : 'opacity-0'} inline`">Loading...</span>
    </p>
  </div>
</template>

<script>
  export default {
    data: () => ({
      loading: false
    }),
    methods: {
      start() {
        this.loading = true
      },
      finish() {
        this.loading = false
      }
    }
  }
</script>

<style>
  path.loader {
    fill: #A61E17;
  }
  @media (prefers-color-scheme: dark) {
    path.loader { fill: #00B4E6; }
  }
</style>
