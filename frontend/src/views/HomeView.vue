<script setup lang="ts">
import Hero from "@/components/Hero.vue";
</script>

<template>
  <main>
    <Hero />
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 71px);
  background-color: var(--color-background-primary);
}
</style>
