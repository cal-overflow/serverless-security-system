<template>
  <div>
    <video-feed type="motion" />
    <camera-overview />
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  middleware: 'authenticate',
}
</script>
