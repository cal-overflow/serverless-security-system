<template>
  <div></div>
</template>

<script>
export default {
  name: 'IndexPage',
  middleware: 'authenticate',
  asyncData({ redirect}) {
    redirect('/footage/all');
  }
}
</script>
