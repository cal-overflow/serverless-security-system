<template>
  <overlay :title="title" @close="exit">
    <div class="px-4">
      <slot />
      <div class="w-full flex justify-between">
        <button
          class="rounded-md py-1 px-2 my-4 bg-gray-400 text-white transition duration-1000"
          @click="deny"
        >
          {{ denyLabel }}
        </button>
        <button
          class="rounded-md py-1 px-2 my-4 bg-primary-light dark:bg-primary-dark text-white transition duration-1000"
          @click="confirm"
        >
          {{ confirmLabel }}
        </button>
      </div>
    </div>
  </overlay>
</template>

<script>
export default {
  name: 'Confirmation',
  props: {
    title: {
      type: String,
      default: 'Prompt',
    },
    denyLabel: {
      type: String,
      default: 'Cancel',
    },
    confirmLabel: {
      type: String,
      default: 'Confirm',
    },
  },
  methods: {
    exit() {
      this.$emit('close');
    },
    confirm() {
      this.$emit('confirm');
    },
    deny() {
      this.$emit('deny');
    },
  },
};
</script>
