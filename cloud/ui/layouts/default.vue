<template>
  <div class="bg-main-light dark:bg-main-dark dark:text-white transition">
    <nav-bar :current-route="$route" />
    <Nuxt />
    <footer-bar />
  </div>
</template>

<style>
html {
  background: #292929;
  scroll-behavior: smooth;
}
</style>
