<template>
  <div>
    <video-feed initialType="all" :descriptionText="`${initialDateFilter} Footage`" :initialDateFilter="initialDateFilter" />
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  middleware: 'authenticate',
  asyncData({ params, query }) {
    const lastForwardSlashIndex = params.pathMatch.includes('/') ? params.pathMatch.lastIndexOf('/') : params.pathMatch.length;
    const directory = params.pathMatch.slice(0, lastForwardSlashIndex);

    return {
      initialDateFilter: directory,
      type: query.type || 'motion'
    };
  }
}
</script>
