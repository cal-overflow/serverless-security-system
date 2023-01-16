<template>
  <div id="nav-bar" class="bg-menu-light dark:bg-menu-dark transition">
    <nav class="mx-auto max-w-6xl flex items-center justify-between flex-wrap p-4 py-6 px-5">
      <nav-item
        :href="signatureHeader.href"
        :active="currentPage === 'Home'"
        class="font-bold">
        {{ signatureHeader.title }}
      </nav-item>
        
      <div class="justify-between">
        <nav-item
          v-for="item in items"
          :key="item.title"
          :href="item.href"
          :active="currentPage === item.title"
        >
          {{ item.title }}
        </nav-item>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'nav-bar',
  props: {
    currentPage: {
      type: String,
      default: ''
    }
  },
  data: () => ({
    signatureHeader: {
      title: 'Security System',
      href: '/'
    },
    items: [
      {
        title: 'Cameras',
        href: '/cameras'
      },
      {
        title: 'Footage',
        href: '/footage'
      },
      {
        title: 'System configuration',
        href: '/config'
      },
      {
        title: 'Users',
        href: '/users'
      },
    ],
  })
};
</script>
