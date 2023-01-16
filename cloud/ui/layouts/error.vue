<template>
  <main>
    <div class="max-w-screen-lg mx-auto">
      <div id="error-main-info-card" class="bg-card-light dark:bg-card-dark m-6 p-4 px-6 flex-wrap shadow-lg hover:shadow-none hover:rounded motion-safe:animate-fade-in transition">
        <div class="text-center">
          <p class="text-sm mb-2">Error</p>
          <p class="text-5xl font-bold motion-safe:animate-blur-fade-in">{{error.statusCode}}</p>
          </div>

        <p class="text-4xl my-6 text-center">{{message}}</p>

        <div class="text-center">
          <nuxt-link ref="back-home" to="/" class="text-primary-light underline hover:no-underline dark:text-primary-dark transition">Take me home</nuxt-link>
        </div>
      </div>

      <div id="error-more-info-card" class="bg-card-light dark:bg-card-dark m-6 p-4 px-6 flex-wrap shadow-lg hover:shadow-none hover:rounded motion-safe:animate-fade-in transition">
        <div>
          <p class="font-bold text-2xl">More information 🤓</p>
          <pre class="text-extra-gray-dark dark:text-extra-gray-light whitespace-normal transition">
            {{extraInfo}}
          </pre>

          <p class="mt-2">If you believe there has been a mistake, please <a href="https://github.com/cal-overflow/serverless-security-system/issues/new" class="text-primary-light underline hover:no-underline dark:text-primary-dark transition" target="_blank">submit an issue</a>.</p>
        </div>
      </div>

    </div>
  </main>
</template>

<script>
export default {
  name: 'error',
  props: {
    error: {
      type: Object,
      required: true,
    },
  },
  computed: {
    message() {
      switch (this.error?.statusCode) {
      case 404:
        return this.error.message || 'Page not found';
      case 500:
        return this.error.message || 'Something went wrong';
      default:
        return this.error.message || 'Something went wrong';
      }
    },
    extraInfo() {
      if (this.error?.error)
        return this.error.error.message;
      
      if (this.error?.statusCode === 404)
        return "The resource you're looking for does not exist.";

      return 'No more information is available 😕';
    },
  }
};
</script>
