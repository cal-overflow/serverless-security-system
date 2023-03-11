<template>
  <overlay :title="title" @close="exit">
    <div class="px-4">
      <slot />
    </div>
  </overlay>
</template>

<script>
export default {
  name: 'Alert',
  props: {
    title: {
      type: String,
      default: 'Prompt',
    },
  },
  methods: {
    exit() {
      this.$emit('close');
    },
  },
};
</script>
