<template>
  <div class="max-w-screen-lg mx-auto">
    <div class="bg-card-light dark:bg-card-dark m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
      <p class="text-2xl font-bold">
        Home
      </p>
    </div>
    <video-feed type="activity" descriptionText="Recent footage" :initialDateFilter="initialDateFilter" />
    <camera-overview />
  </div>
</template>

<script>
const formatNumber = (num) => {
  return num.toLocaleString('en-US', {
    minimumIntegerDigits: 2,
    useGrouping: false
  });
};


const today = new Date();

export default {
  name: 'IndexPage',
  middleware: 'authenticate',
  data: () => ({
    initialDateFilter: `${today.getFullYear()}-${formatNumber(today.getMonth() + 1)}-${formatNumber(today.getDate())}`
  }),
}
</script>
