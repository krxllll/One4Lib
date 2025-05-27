<script setup lang="ts">
import { useRoute } from "vue-router";
import {onMounted, ref} from "vue";
import PointIcon from "@/components/icons/PointIcon.vue";
import StarIcon from "@/components/icons/StarIcon.vue";

const route = useRoute();
const id = Number(route.params.id);
const file = ref();

onMounted(() => {
  file.value = {
    title: "Sample File",
    author: "author_username",
    price: 10,
    type: "PDF",
    rating: 5,
    description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusantium aliquid assumenda at cum dolores dolorum eos esse exercitationem explicabo itaque iure libero minus, necessitatibus nulla obcaecati odit perspiciatis provident quibusdam quis quisquam, quod ratione reiciendis reprehenderit rerum saepe sed tempore, veritatis vitae voluptas voluptatibus. Aliquam consequatur earum eius excepturi itaque iusto nesciunt, qui ut voluptatibus! A assumenda blanditiis eum illo molestiae nam natus repudiandae voluptas! A eligendi in necessitatibus reiciendis sunt vel, veniam? Dicta esse est quibusdam sed. Aspernatur consectetur cumque magni molestiae natus provident rerum, sunt tenetur ut vitae? Ab, aliquid beatae consequatur cum cupiditate, debitis esse et fuga maxime nisi nobis perspiciatis, possimus recusandae reiciendis saepe? Asperiores blanditiis delectus deserunt fugit impedit iste iusto minima neque perspiciatis porro, voluptatibus voluptatum. Ad alias, aperiam at beatae deleniti doloremque dolorum earum eum ex id inventore labore magnam maiores maxime molestiae nihil porro repudiandae saepe sed sunt velit, vero vitae voluptatem.",
    thumbnail: "https://placehold.co/340x340?text=Preview&font=roboto",
    preview: "/sample.mp3",
  };
});

const fileTypes = ['pdf', 'doc', 'xlsx', 'jpg', 'png', 'svg', 'mp3', 'mp4', 'py', 'cpp'] as const
type FileType = typeof fileTypes[number]

const getColorClass = (type: FileType): string => {
  const t = type.toLowerCase()
  if (['pdf', 'doc', 'xlsx'].includes(t)) return 'bg-green'
  if (['jpg', 'png', 'svg'].includes(t)) return 'bg-red'
  if (['mp3', 'mp4'].includes(t)) return 'bg-blue'
  if (['py', 'cpp'].includes(t)) return 'bg-purple'
  return 'unselected'
}

const toggleWishlist = () => {
  const wishlistButton = document.querySelector('.wishlist') as HTMLButtonElement;
  if (wishlistButton) {
    wishlistButton.classList.toggle('active');
    wishlistButton.textContent = wishlistButton.classList.contains('active') ? 'Remove from wishlist' : 'Add to wishlist';
  }
}
</script>

<template>
  <div class="container" v-if="file">
    <div class="thumbnail">
      <img :src="file.thumbnail" alt="File Thumbnail" />
    </div>
    <div class="content">
      <div class="header">
        <h1 class="title">
          {{ file.title }}
        </h1>
        <div class="subtitle">
          <h2 class="autor">
            {{ file.author }}
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
          <div :class="['type', getColorClass(file.type)]">
            <p>{{ file.type }}</p>
          </div>
          <div class="rating">
            <p>{{ file.rating/2 }}</p>
            <StarIcon :rating=file.rating height="24" width="24" viewBox="0 0 24 24" class="icon"/>
          </div>
        </div>
        <div class="actions">
          <button class="buy btn">Buy</button>
          <button class="btn">Download</button>
          <div class="rate-btn">
            <StarIcon :rating=0 height="24" width="24" viewBox="0 0 24 24" class="icon"/>
            <StarIcon :rating=0 height="24" width="24" viewBox="0 0 24 24" class="icon"/>
            <StarIcon :rating=0 height="24" width="24" viewBox="0 0 24 24" class="icon"/>
            <StarIcon :rating=0 height="24" width="24" viewBox="0 0 24 24" class="icon"/>
            <StarIcon :rating=0 height="24" width="24" viewBox="0 0 24 24" class="icon"/>
          </div>
        </div>
      </div>
    </div>
    <div class="preview-description">
      <div class="preview">
        <iframe :src="file.preview" width="100%" height="100%" allowfullscreen></iframe>
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
.autor {
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
</style>
