<template>
  <div class="max-w-screen-lg mx-auto bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
    <div>
      <p class="text-xl font-bold">{{user.name}}</p>
      <p class="text-md"><span class="font-bold">Pin:</span> {{user.pin}}</p>
      <p class="text-md"><span class="font-bold">Admin:</span> {{user.admin}}</p>
    </div>
  </div>
</template>


<script>
export default {
  name: 'user-card',
  props: {
    user: {
      type: Object,
      required: true
    }
  }
}
</script>

