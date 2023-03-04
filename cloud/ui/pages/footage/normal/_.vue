<template>
  <div>
    <video-feed initialType="normal" :descriptionText="`${initialDateFilter} Footage without motion`" :initialDateFilter="initialDateFilter" :initialCamera="$route.query.camera" />
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  middleware: 'authenticate',
  asyncData({ params }) {
    const lastForwardSlashIndex = params.pathMatch.includes('/') ? params.pathMatch.lastIndexOf('/') : params.pathMatch.length;
    const directory = params.pathMatch.slice(0, lastForwardSlashIndex);

    return {
      initialDateFilter: directory,
    };
  }
}
</script>
