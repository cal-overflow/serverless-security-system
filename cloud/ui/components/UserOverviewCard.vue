<template>
  <div
    @mouseover="mouseover = true"
    @mouseleave="mouseover = false"
    class="flex flex-wrap md:flex-none
           bg-card-light dark:bg-card-dark
           p-8 sm:p-4 mx-auto
           sm:w-full md:shadow-lg md:dark:shadow-shadow-dark
           hover:shadow-none hover:rounded
           static
           motion-safe:animate-fade-in-fast transition"
  >
    <div class="text-center md:text-left mb-8 w-full">
      <p class="text-xl font-bold">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="inline w-16 md:w-8 h-auto">
          <path d="M4.5 6.375a4.125 4.125 0 118.25 0 4.125 4.125 0 01-8.25 0zM14.25 8.625a3.375 3.375 0 116.75 0 3.375 3.375 0 01-6.75 0zM1.5 19.125a7.125 7.125 0 0114.25 0v.003l-.001.119a.75.75 0 01-.363.63 13.067 13.067 0 01-6.761 1.873c-2.472 0-4.786-.684-6.76-1.873a.75.75 0 01-.364-.63l-.001-.122zM17.25 19.128l-.001.144a2.25 2.25 0 01-.233.96 10.088 10.088 0 005.06-1.01.75.75 0 00.42-.643 4.875 4.875 0 00-6.957-4.611 8.586 8.586 0 011.71 5.157v.003z" />
        </svg>
        <br class="block md:hidden" />
        Users
      </p>
    </div>
    <div class="w-full text-center">
      <p class="text-4xl">
        <svg v-if="users.length >= 3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-2/5 md:w-1/3 text-primary-light dark:text-primary-dark motion-safe:animate-fade-in">
          <path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
        </svg>
        <svg v-else-if="users.length === 2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-2/5 md:w-1/3 text-primary-light dark:text-primary-dark motion-safe:animate-fade-in">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline w-2/5 md:w-1/3 text-primary-light dark:text-primary-dark motion-safe:animate-fade-in">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
        </svg>
        <br />
        {{users.length}} Users
      </p>
      <p class="text-sm text-extra-gray-dark dark:text-extra-gray-light">
        {{adminDisplayCount}}
      </p>
      <div class="text-center my-2">
        <nuxt-link to="/users" class="text-primary-light dark:text-primary-dark underline hover:no-underline">
          Dashboard
        </nuxt-link>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'user-overview-card',
  props: {
    users: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    linkhover: false,
    adminUserCount: 0,
    adminDisplayCount: 'no admins',
  }),
  mounted() {
    let adminCount = 0;

    this.users.forEach((user) => {
      if (user.admin) {
        adminCount++;
      }
    });

    this.adminCount = adminCount;
    this.adminDisplayCount = `${adminCount} admin${adminCount === 1 ? '' : 's'}`;
  },
}
</script>
