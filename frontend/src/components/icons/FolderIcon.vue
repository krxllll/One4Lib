<script setup lang="ts">
import { defineProps } from 'vue';
defineProps({
  height: {
    type: [String, Number],
    default: 24,
  },
  width: {
    type: [String, Number],
    default: 24,
  },
  viewBox: {
    type: String,
    default: "0 0 512 512",
  }
});
</script>

<template>
  <svg
    :height="height"
    :width="width"
    :viewBox="viewBox"
    xmlns="http://www.w3.org/2000/svg">
    <g>
      <path fill="currentColor" d="m490.6,158.7h-62.6v-38.7c0-5.8-4.7-10.4-10.4-10.4h-223.2l-26.9-56.1c-1.7-3.6-5.4-5.9-9.4-5.9h-136.7c-5.8,0-10.4,4.7-10.4,10.4v396.2c0.3,8.7 8.3,10.7 10.4,10.4h396.2c4.8,0 8.9-3.2 10.1-7.8l73-285c1.5-3.7-0.9-12.9-10.1-13.1zm-458.7-90.4h119.6l26.9,56.1c1.7,3.6 5.4,5.9 9.4,5.9h219.4v28.3h-312.8c-4.8,0-8.9,3.2-10.1,7.8l-52.4,204.9v-303zm377.6,375.4h-374.6l67.6-264.1h374.6l-67.6,264.1z"/>
    </g>
  </svg>
</template>
