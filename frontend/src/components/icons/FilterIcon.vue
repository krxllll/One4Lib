<script setup lang="ts">
import { defineProps } from 'vue';
defineProps({
  height: {
    type: [String, Number],
    default: 17,
  },
  width: {
    type: [String, Number],
    default: 17,
  },
  viewBox: {
    type: String,
    default: "0 0 17 17",
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
    <path d="M15.5832 1.125H1.4165L7.08317 7.82583V12.4583L9.9165 13.875V7.82583L15.5832 1.125Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</template>
