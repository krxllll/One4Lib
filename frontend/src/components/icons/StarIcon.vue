<script setup lang="ts">
import { defineProps, computed } from 'vue';

const props = defineProps({
  rating: {
    type: Number,
    required: true,
    validator: (val: number) => val >= 0 && val <= 10,
  },
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
    default: "0 0 24 24",
  }
});

const fillPercent = computed(() => `${(props.rating / 10) * 100}%`)
</script>

<template>
  <div style="position: relative; display: inline-block;" :style="{ width: width + 'px', height: height + 'px' }">
    <svg
      :height="height"
      :width="width"
      :viewBox="viewBox"
      style="position: absolute; top: 0; left: 0;"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path d="M 12.001 0.418 C 12.418 0.418 12.798 0.652 12.978 1.029 L 16.082 7.421 L 23.013 8.444 C 23.42 8.502 23.759 8.788 23.885 9.182 C 24.012 9.575 23.908 10 23.619 10.29 L 18.591 15.275 L 19.777 22.314 C 19.846 22.721 19.678 23.133 19.338 23.378 C 19 23.622 18.556 23.648 18.194 23.454 L 11.996 20.143 L 5.807 23.449 C 5.441 23.643 4.996 23.617 4.664 23.373 C 4.327 23.129 4.156 22.716 4.224 22.309 L 5.408 15.27 L 0.383 10.29 C 0.088 10 -0.011 9.57 0.117 9.182 C 0.243 8.792 0.582 8.507 0.989 8.444 L 7.92 7.421 L 11.023 1.029 C 11.209 0.652 11.584 0.418 12.001 0.418 Z M 11.997 0.852 L 8.789 7.464 C 8.575 7.9 8.162 8.206 7.683 8.28 L 0.449 9.343 L 5.702 14.546 C 6.036 14.883 6.195 15.359 6.114 15.828 L 4.875 23.148 L 11.305 19.713 C 11.739 19.477 12.261 19.477 12.687 19.713 L 19.118 23.148 L 17.883 15.835 C 17.804 15.368 17.959 14.889 18.299 14.552 L 23.551 9.35 L 16.322 8.28 C 15.842 8.206 15.426 7.905 15.214 7.464 L 11.997 0.852 Z" fill="currentColor"></path>
    </svg>

    <div :style="{
      width: fillPercent,
      overflow: 'hidden',
      position: 'absolute',
      top: 0,
      left: 0,
      height: '100%'
    }">
      <svg
        :width="width"
        :height="height"
        :viewBox="viewBox"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M 12.001 0.418 C 12.418 0.418 12.798 0.652 12.978 1.029 L 16.082 7.421 L 23.013 8.444 C 23.42 8.502 23.759 8.788 23.885 9.182 C 24.012 9.575 23.908 10 23.619 10.29 L 18.591 15.275 L 19.777 22.314 C 19.846 22.721 19.678 23.133 19.338 23.378 C 19 23.622 18.556 23.648 18.194 23.454 L 11.996 20.143 L 5.807 23.449 C 5.441 23.643 4.996 23.617 4.664 23.373 C 4.327 23.129 4.156 22.716 4.224 22.309 L 5.408 15.27 L 0.383 10.29 C 0.088 10 -0.011 9.57 0.117 9.182 C 0.243 8.792 0.582 8.507 0.989 8.444 L 7.92 7.421 L 11.023 1.029 C 11.209 0.652 11.584 0.418 12.001 0.418 Z" fill="currentColor"></path>
      </svg>
    </div>
  </div>
</template>
