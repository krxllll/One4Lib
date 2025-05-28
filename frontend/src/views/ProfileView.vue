<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();
function logout() {
  auth.logout();
  router.push({ name: "login" });
}
</script>

<template>
  <main class="container">
    <div class="future-content">
      <h1>In future here will be:</h1>
      <ul>
        <li>Profile Settings</li>
        <li>Account Settings</li>
        <li>Notifications</li>
        <li>Transactions History</li>
      </ul>
    </div>
    <button class="btn" @click="logout">Log out</button>
  </main>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 71px);
  background-color: var(--color-background-primary);
  gap: 32px;
}
.future-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
li {
  margin-bottom: 8px;
}
</style>
