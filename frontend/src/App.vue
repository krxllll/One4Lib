<script setup lang="ts">
import { RouterView, useRoute, useRouter } from 'vue-router'
import Navbar from "@/components/Navbar.vue";
import BackIcon from "@/components/icons/BackIcon.vue";
const route = useRoute();
const router = useRouter();

function goBack() {
  router.back();
}
</script>

<template>
  <button v-if="['login', 'registration'].includes(route.name as string)" class="back-button" @click="goBack">
    <BackIcon width="35" height="20" viewBox="0 0 14 8"/>
  </button>
  <Navbar v-if="!['login', 'registration'].includes(route.name as string)" />
  <RouterView />
</template>

<style scoped>
.back-button {
  position: fixed;
  top: 40px;
  left: 32px;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 1000;
  color: var(--color-white);
}
.back-button:hover {
  color: var(--color-accent);
}
</style>
