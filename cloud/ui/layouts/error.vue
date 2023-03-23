<template>
  <main>
    <div class="max-w-screen-lg mx-auto">
      <div
        class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition"
      >
        <p class="text-4xl font-bold text-center md:text-left">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="inline text-primary-light dark:text-primary-dark w-24 md:w-16 h-auto"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
            />
          </svg>
          <br class="block md:hidden" />
          Error
        </p>
      </div>
      <div
        id="error-main-info-card"
        class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition"
      >
        <div class="text-center">
          <p class="text-md">Status code</p>
          <p class="text-5xl font-bold motion-safe:animate-blur-fade-in">
            {{ error.statusCode }}
          </p>
          <p class="my-6 text-center">{{ message }}</p>
          <nuxt-link
            ref="back-home"
            to="/"
            class="text-primary-light underline hover:no-underline dark:text-primary-dark transition"
          >
            Take me home
          </nuxt-link>
        </div>
      </div>
      <div
        id="error-more-info-card"
        class="bg-card-light dark:bg-card-dark m-0 md:m-6 pt-12 p-6 md:p-4 flex-wrap shadow-lg hover:shadow-none hover:rounded motion-safe:animate-fade-in transition"
      >
        <div>
          <p class="font-bold text-2xl">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="inline w-10 h-10"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
              />
            </svg>
            More information
          </p>
          <pre
            class="text-extra-gray-dark dark:text-extra-gray-light whitespace-normal transition"
          >
            {{ extraInfo }}
          </pre>

          <p class="mt-2">
            If you believe there has been a mistake, please
            <a
              href="https://github.com/cal-overflow/serverless-security-system/issues/new"
              class="text-primary-light underline hover:no-underline dark:text-primary-dark transition"
              target="_blank"
              >submit an issue</a
            >.
          </p>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  name: 'Error',
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
      if (this.error?.error) return this.error.error.message;

      if (this.error?.statusCode === 404)
        return "The resource you're looking for does not exist.";

      return 'No more information is available 😕';
    },
  },
};
</script>
