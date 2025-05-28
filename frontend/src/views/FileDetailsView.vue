<script setup lang="ts">
import { useRoute } from "vue-router";
import { onMounted, ref } from "vue";
import { api } from "@/utils/api.ts";
import axios from "axios";
import { handleApiError } from "@/utils/handleApiError.ts";
import PointIcon from "@/components/icons/PointIcon.vue";
import StarIcon from "@/components/icons/StarIcon.vue";
import {type File, type FileType, fileTypeColors} from "@/types/file.ts";
import router from "@/router";
import { useAuthStore } from "@/stores/auth.ts";

const route = useRoute();
const id = route.params.id as string;
const file = ref<File>();
const isOwned = ref(false);
const auth = useAuthStore()

onMounted(async () => {
  try {
    const {data} = await api.get(`/files/${id}`);
    file.value = data;
    data.viewer_status === 'author' || data.viewer_status === 'owner' ? isOwned.value = true : isOwned.value = false;
  } catch (err) {
    const message = handleApiError(err, 'Fetching file details failed')
    console.error('Error while fetching file details:', message)
  }
});

const getColorClass = (type: FileType): string => {
  const t = type.toLowerCase().split('/')[0]
  return fileTypeColors[t] || 'unselected'
}

const toggleWishlist = () => {
  const wishlistButton = document.querySelector('.wishlist') as HTMLButtonElement;
  if (wishlistButton) {
    wishlistButton.classList.toggle('active');
    wishlistButton.textContent = wishlistButton.classList.contains('active') ? 'Remove from wishlist' : 'Add to wishlist';
  }
}

const buyFile = async () => {
  if (isOwned.value) return
  try {
    const response = await api.post('/file-purchase/file', { file_id: id })
    if (response.status === 204) {
      console.log('File purchased successfully')
      isOwned.value = true
      await auth.getUserBalance()
    } else {
      console.warn('Unexpected status:', response.status)
    }
  } catch (err) {
    if (axios.isAxiosError(err) && err.response) {
      const status = err.response.status
      if (status === 402) {
        alert('There is not enough balance to purchase the file.')
        await router.push('/shop')
      } else if (status === 422) {
        console.error('Validation error.')
      } else {
        console.error('Other mistake when buying:', status)
      }
    } else {
      console.error('Unknown error during purchase:', err)
    }
  }
}
</script>

<template>
  <div class="container" v-if="file">
    <div class="thumbnail">
      <img :src="file.thumbnail_url" alt="File Thumbnail" />
    </div>
    <div class="content">
      <div class="header">
        <h1 class="title">
          {{ file.title }}
        </h1>
        <div class="subtitle">
          <h2 class="author">
            {{ file.author_username }}
          </h2>
          <button class="wishlist" @click="toggleWishlist">Add to wishlist</button>
        </div>
      </div>
      <div class="details">
        <div class="info">
          <div class="price">
            <p>{{ file.price }}</p>
            <PointIcon height="36" width="36" viewBox="0 0 24 24" class="icon"/>
          </div>
          <div :class="['type', getColorClass(file.file_type)]">
            <p>{{ file.file_type.split('/')[1].toUpperCase() }}</p>
          </div>
          <div class="rating">
            <p>{{ 4.5 }}</p>
            <StarIcon :rating=9 height="24" width="24" viewBox="0 0 24 24" class="icon"/>
          </div>
        </div>
        <div class="actions">
          <button class="buy btn" :disabled="isOwned" @click="buyFile">{{ isOwned ? 'Owned' : 'Buy' }}</button>
          <button class="btn" :disabled="!isOwned">Download</button>
          <div class="rate-btn">
            <StarIcon v-for="i in 5" :key="i" :rating=0 height="24" width="24" viewBox="0 0 24 24" class="icon"/>
          </div>
        </div>
      </div>
    </div>
    <div class="preview-description">
      <div class="preview">
        <iframe :src="file.preview_url" width="100%" height="100%" allowfullscreen></iframe>
      </div>
      <div class="description">
        <p>{{ file.description }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  gap: 32px;
  background: linear-gradient(180deg, var(--color-background-primary), var(--color-black) 100%);
}
.thumbnail {
  width: 100%;
  height: 275px;
  position: relative;
  overflow: hidden;
}
.thumbnail img {
  width: 100%;
  height: auto;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  filter: blur(8px);
}
.content, .preview-description {
  width: 100%;
  display: flex;
  gap: 64px;
}
.header {
  display: flex;
  flex-direction: column;
  gap: 14px;
  flex: 1;
}
.title {
  font-size: 40px;
  font-weight: 275;
  color: var(--color-white);
}
.subtitle {
  display: flex;
  justify-content: space-between;
  align-items: end;
}
.wishlist {
  color: var(--color-white);
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  text-decoration-line: underline;
  text-underline-offset: 3px;
  font-family: var(--font-btn), sans-serif;
  background: none;
  border: none;
  cursor: pointer;
}
.wishlist.active {
  color: var(--color-accent);
}
.author {
  font-size: 24px;
  line-height: 24px;
  font-weight: 200;
  color: var(--color-accent);
  font-family: var(--font-btn), sans-serif;
}
.details {
  display: flex;
  flex-direction: column;
  width: 35%;
  gap: 16px;
}
.actions {
  display: flex;
  align-items: center;
  gap: 16px;
}
.rate-btn {
  display: flex;
  align-items: center;
  gap: 2px;
  margin-left: auto;
}
.info {
  display: flex;
  align-items: end;
  gap: 16px;
}
.price {
  display: flex;
  align-items: center;
  gap: 8px;
}
.price .icon {
  color: var(--color-accent);
}
.price p {
  font-size: 40px;
  font-family: var(--font-btn), sans-serif;
  font-weight: 600;
  color: var(--color-white);
  line-height: 40px;
}
.type {
  padding: 0 16px;
  height: 40px;
  display: flex;
  align-items: center;
  border-radius: 20px;
}
.type p {
  line-height: 13px;
  font-size: 16px;
  font-weight: 400;
  color: var(--color-white);
  font-family: var(--font-btn), sans-serif;
  letter-spacing: 0.5px;
}
.rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}
.rating p {
  font-size: 28px;
  font-weight: 600;
  color: var(--color-white);
  font-family: var(--font-btn), sans-serif;
  line-height: 28px;
}
.rating .icon {
  color: var(--color-accent);
}
.preview {
  flex: 1;
  height: 768px;
}
.description {
  width: 35%;
}
.description p {
  font-size: 18px;
  font-weight: 200;
}
.buy {
  background-color: var(--color-accent);
}
.buy:hover {
  background-color: var(--color-background-secondary);
}
.buy:disabled {
  background-color: var(--color-placeholder-secondary);
  color: var(--color-placeholder-primary);
  border-color: var(--color-placeholder-secondary);
  cursor: not-allowed;
}
</style>
