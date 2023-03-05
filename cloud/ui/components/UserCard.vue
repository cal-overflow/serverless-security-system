<template>
  <div
    v-if="user"
    @mouseover="mouseover = true"
    @mouseleave="mouseover = false"
    class="flex flex-wrap md:flex-none
           bg-card-light dark:bg-card-dark
           p-8 sm:p-4 mx-auto
           sm:w-full md:shadow-lg md:dark:shadow-shadow-dark
           hover:shadow-none hover:rounded
           motion-safe:animate-fade-in-fast transition"
  >
    <svg xmlns="http://www.w3.org/2000/svg" :fill="isAuthenticated ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" :class="`w-2/3 mx-auto h-auto fill-primary-light dark:fill-primary-dark ${isAuthenticated ? 'text-primary-light dark:text-primary-dark ' : ''}`">
      <path v-if="isAuthenticated" stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
      <path v-else stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
    <div class="w-full">
      <div class="flex sm:flex-none justify-between w-full">
        <p class="text-2xl font-bold">
          {{user.name}}
        </p>
        <button v-if="canEdit" @click.prevent="edit" class="py-1 px-2 hover:text-primary-light dark:hover:text-primary-dark transition duration-500 rounded-full">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />
          </svg>
        </button>
      </div>
      <p class="text-md"><span class="font-bold">Pin:</span> {{pin}}</p>
      <p class="text-md"><span class="font-bold">Admin:</span> {{user.admin}}</p>
    </div>
  </div>
  <div
    v-else
    @mouseover="mouseover = true"
    @mouseleave="mouseover = false"
    class="flex flex-wrap md:flex-none
           bg-primary-light dark:bg-primary-dark text-white
           p-8 sm:p-4 mx-auto
           sm:w-full md:shadow-lg md:dark:shadow-shadow-dark
           hover:shadow-none hover:rounded
           cursor-pointer
           motion-safe:animate-fade-in-fast transition"
  >
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-2/3 mx-auto h-auto">
      <path stroke-linecap="round" stroke-linejoin="round" d="M19 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM4 19.235v-.11a6.375 6.375 0 0112.75 0v.109A12.318 12.318 0 0110.374 21c-2.331 0-4.512-.645-6.374-1.766z" />
    </svg>
    <div class="w-full">
      <div class="flex sm:flex-none justify-between w-full">
        <p class="text-2xl font-bold">
          Invite user
        </p>
      </div>
      <p class="text-md"><span class="font-bold">TODO&nbsp;</span></p>
      <p class="text-md"><span class="font-bold">&nbsp;</span></p>
    </div>
  </div>
</template>


<script>
export default {
  name: 'user-card',
  props: {
    user: {
      type: Object,
      required: false
    },
    canEdit: {
      type: Boolean,
      default: false
    },
    isAuthenticated: {
      type: Boolean,
      default: false
    },
  },
  data: () => ({
    mouseover: false,
  }),
  mounted() {
    if (this.user) {
      this.nameEdit = this.user.name;
      this.adminEdit = this.user.admin;
    }
  },
  computed: {
    pin() {
      return this.user.pin || '****';
    }
  },
  methods: {
    edit() {
      this.$emit('edit');
    }
  }
}
</script>

