<script setup lang="ts">
import { defineProps } from 'vue';
defineProps({
  height: {
    type: [String, Number],
    default: 8,
  },
  width: {
    type: [String, Number],
    default: 14,
  },
  viewBox: {
    type: String,
    default: "0 0 14 8",
  }
});
</script>

<template>
  <svg
    :height="height"
    :width="width"
    :viewBox="viewBox"
    fill="none"
    xmlns="http://www.w3.org/2000/svg">
    <path d="M0.646446 3.64645C0.451184 3.84171 0.451184 4.15829 0.646446 4.35356L3.82843 7.53554C4.02369 7.7308 4.34027 7.7308 4.53553 7.53554C4.7308 7.34027 4.7308 7.02369 4.53553 6.82843L1.70711 4L4.53553 1.17157C4.7308 0.976312 4.7308 0.65973 4.53553 0.464467C4.34027 0.269205 4.02369 0.269205 3.82843 0.464468L0.646446 3.64645ZM14 4L14 3.5L1 3.5L1 4L1 4.5L14 4.5L14 4Z" fill="currentColor"/>
  </svg>
</template>
