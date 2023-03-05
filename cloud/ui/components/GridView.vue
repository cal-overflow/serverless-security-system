<template>
  <div class="max-w-screen-lg mx-auto">
    <div class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
      <p class="text-4xl font-bold text-center md:text-left">
        {{title}}
      </p>
    </div>
    <div
      class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 md:p-0
             md:bg-main-light md:dark:bg-main-dark grid sm:grid-cols-2 md:grid-cols-3 justify-center sm:justify-between gap-4 md:gap-10
             motion-safe:animate-fade-in-fast transition"
    >
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'grid-view',
  props: {
    title: {
      type: String,
      required: true
    },
  },
}
</script>
