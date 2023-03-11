<template>
  <div class="w-screen h-screen z-40 flex fixed top-0 left-0 p-0 m-0 bg-card-light dark:bg-card-dark sm:bg-gray-500 sm:bg-opacity-70">
    <div
      class="w-full sm:w-3/4 md:w-3/5 max-w-screen-sm
             p-6 mx-auto my-auto
             h-full sm:h-auto
             flex flex-col sm:flex-none justify-between
             bg-card-light dark:bg-card-dark"
    >
      <div class="w-full flex justify-between flex-nowrap pb-4">
        <p class="text-3xl font-bold">
          {{title}}
        </p>
        <button @click="exit" class="text-primary-light dark:text-primary-dark">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
      </div>
      <div>
        <slot />
      </div>
      <div class="block sm:hidden">
        <!-- This div is a spacer for small screens! -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'overlay',
  props: {
    title: {
      type: String,
      default: "Prompt"
    }
  },
  methods: {
    exit() {
      this.$emit('close');
    }
  }
}
</script>
