<script setup lang="ts">
import { defineProps } from 'vue';
defineProps({
  title: {
    type: String,
    default: 'File Thumbnail',
    required: true,
  },
  type: {
    type: String,
    default: 'jpg',
    required: true,
  },
  imageUrl: {
    type: String,
    default: 'https://placehold.co/340x340?text=Hello&font=roboto',
    required: true,
  },
});
</script>

<template>
  <div class="file-thumbnail">
    <div class="title">
      <p>{{ title }}</p>
      <p>{{ type.toUpperCase() }}</p>
    </div>
    <div class="thumbnail">
      <img :src=imageUrl alt="File Thumbnail" />
    </div>
  </div>
</template>

<style scoped>
.file-thumbnail {
  position: relative;
  width: 340px;
  height: 340px;
  border-radius: 32px;
  cursor: pointer;
}
.title {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  padding: 16px 30px;
  border-radius: 32px 32px 0 0;
  background: color-mix(in srgb, var(--color-placeholder-secondary) 65%, transparent);
  backdrop-filter: blur(12px);
  z-index: 1;
  display: flex;
  justify-content: space-between;
}
.title p {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-white);
}
.thumbnail {
  width: 100%;
  height: 100%;
  border-radius: 32px;
  overflow: hidden;
  position: relative;
}
.thumbnail img {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}
</style>
