<template>
  <div class="bg-footer text-white">
    <nav id="footer-bar" class="w-full max-w-screen-lg mx-auto px-8 py-6 px-5 flex items-center justify-between flex-wrap motion-safe:animate-fade-in-slow">
      <div>
        <nav-item
          v-for="item in items"
          :key="item.title"
          :href="item.href"
        >
          {{ item.title }}
        </nav-item>
      </div>

      <div>
        <a id="github-link" href="https://github.com/cal-overflow/serverless-security-system" target="_blank" title="View the Github repository for this system">
          <img id="github-logo" class="aspect-square w-6 h-auto inline align-middle mx-4" src="~/assets/images/github.png" />
        </a>
      </div>

    </nav>
  </div>
</template>

<script>
export default {
  name: 'footer-bar',
  props: {
    currentPage: {
      type: String,
      default: ''
    }
  },
  data: () => ({
    items: [
      {
        title: 'Home',
        href: '/'
      },
      {
        title: 'Logout',
        href: '/logout'
      }
    ]
  }),
};
</script>
