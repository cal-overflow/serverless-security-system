<template>
  <overlay :title="title" v-on:close="exit">
  <div class="px-4">
    <slot />
  </div>
  </overlay>
</template>

<script>
export default {
  name: 'alert',
  props: {
    title: {
      type: String,
      default: "Prompt"
    },
  },
  methods: {
    exit() {
      this.$emit('close');
    },
  }
}
</script>
