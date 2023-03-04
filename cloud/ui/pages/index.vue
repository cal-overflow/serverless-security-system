<template>
  <div>
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
