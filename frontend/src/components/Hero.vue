<script setup lang="ts">

</script>

<template>
  <section class="container">
    <div class="content">
      <div class="title">
        <h1><span>Take</span> Files, <span>Share</span> Files</h1>
        <p>Find any file you need - download it.</p>
      </div>
      <router-link to="/search" custom v-slot="{ navigate }">
        <button @click="navigate" class="btn">Get Started</button>
      </router-link>
    </div>
    <div class="image"></div>
  </section>
</template>

<style scoped>
.container {
  height: 80vh;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}
.content {
  flex: 6;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 50px 120px 120px 50px;
  gap: 64px;
}
.image {
  flex: 4;
  height: 100%;
  background-image: url('@/assets/img/hero-image.png');
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}
.title > h1 {
  font-size: 64px;
  font-weight: 275;
  text-transform: uppercase;
}
.title > h1 > span {
  color: var(--color-accent);
}
.title > p {
  font-size: 24px;
  font-weight: 275;
  letter-spacing: 1.44px;
  margin-left: 12px;
}
.btn {
  height: 48px;
  width: 200px;
  font-size: 16px;
  line-height: 48px;
}
</style>
