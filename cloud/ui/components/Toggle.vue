<template>
  <div class="flex items-center justify-center">
    <label for="toggle" class="flex items-center cursor-pointer">
      <!-- toggle -->
      <div class="relative">
        <!-- input -->
        <input
          id="toggle"
          :checked="item"
          type="checkbox"
          class="sr-only"
          @input="handleInput"
        />
        <!-- line -->
        <div
          class="block bg-extra-gray-light dark:bg-extra-gray-dark w-14 h-8 rounded-full"
        ></div>
        <!-- dot -->
        <div
          :class="`dot absolute z-10 left-1 top-1 bg-white w-6 h-6 rounded-full transition ${
            item ? 'bg-primary-light dark:bg-primary-dark' : ''
          }`"
        ></div>
        <!-- label -->
      </div>
      <div
        v-if="showLabel"
        class="ml-3 text-extra-gray-dark dark:text-extra-gray-light"
      >
        {{ label }}
      </div>
    </label>
  </div>
</template>

<script>
export default {
  name: 'Toggle',
  model: {
    prop: 'item',
  },
  props: {
    item: {
      type: Boolean,
      required: true,
    },
    showLabel: {
      type: Boolean,
      default: false,
    },
    onLabel: {
      type: String,
      default: 'On',
    },
    offLabel: {
      type: String,
      default: 'Off',
    },
  },
  computed: {
    label() {
      return this.item ? this.onLabel : this.offLabel;
    },
  },
  methods: {
    handleInput(event) {
      this.$emit('input', event.target.checked);
    },
  },
};
</script>

<style scoped>
input:checked ~ .dot {
  transform: translateX(100%);
}
</style>
