<script setup lang="ts">
import { defineProps } from 'vue';
defineProps({
  height: {
    type: [String, Number],
    default: 16,
  },
  width: {
    type: [String, Number],
    default: 16,
  },
  viewBox: {
    type: String,
    default: "0 0 16 16",
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
    <path d="M5.94824 0C9.23308 0.00014797 11.8955 2.58337 11.8955 5.76953C11.8953 8.95554 9.23297 11.5379 5.94824 11.5381C2.66338 11.5381 0.000177208 8.95563 0 5.76953C0 2.58328 2.66327 0 5.94824 0ZM5.94824 1.50488C3.52022 1.50488 1.55176 3.41448 1.55176 5.76953C1.55193 8.12444 3.52033 10.0332 5.94824 10.0332C8.37602 10.0331 10.3445 8.12435 10.3447 5.76953C10.3447 3.41457 8.37613 1.50503 5.94824 1.50488Z" fill="currentColor"/>
    <rect width="1.53003" height="8.1439" transform="matrix(0.74015 -0.672442 0.694659 0.719339 9.21045 10.1417)" fill="currentColor"/>
  </svg>
</template>
