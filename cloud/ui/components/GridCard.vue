<template>
  <div
    class="flex flex-wrap md:flex-none
           bg-card-light dark:bg-card-dark
           p-8 sm:p-4 mx-auto
           sm:w-full md:shadow-lg md:dark:shadow-shadow-dark
           hover:shadow-none hover:rounded
           static
           motion-safe:animate-fade-in-fast transition"
  >
    <slot />
  </div>
</template>


<script>
export default {
  name: 'grid-card',
}
</script>
