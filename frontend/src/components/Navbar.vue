<script setup lang="ts">
import { defineProps } from 'vue';
import PointIcon from "@/components/icons/PointIcon.vue";
const props = defineProps({
  loggedIn: {
    type: Boolean,
    default: false,
  },
  username: {
    type: String,
    default: 'username',
  },
  balance: {
    type: Number,
    default: 0,
  },
});
</script>

<template>
  <nav class="container">
    <div class="logo">
      <router-link to="/">One<span>4</span>Lib</router-link>
    </div>
    <div class="links">
      <router-link to="/">Home</router-link>
      <router-link to="/search">Search</router-link>
      <router-link to="/library">My Lib</router-link>
      <router-link to="/upload">Upload</router-link>
    </div>
    <div class="user-info">
      <router-link to="/login" v-if="!loggedIn">Login</router-link>
      <router-link to="/signup" class="signup" v-if="!loggedIn">Sign Up</router-link>
      <router-link class="balance" to="" v-if="loggedIn">
        <span>{{ balance }}</span>
        <PointIcon height="16" width="16" viewBox="0 0 24 24" class="icon" />
      </router-link>
      <router-link class="username" to="" v-if="loggedIn">{{ username }}</router-link>
    </div>
  </nav>
</template>

<style scoped>
.container{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  padding-bottom: 16px;
  position: sticky;
  top: 0;
  background-color: var(--color-background-primary);
  z-index: 1000;
}
.logo {
  font-size: 24px;
  font-weight: 275;
  font-family: var(--font-primary), sans-serif;
}
.logo span {
  color: var(--color-accent);
}
.logo a:hover span {
  color: var(--color-white);
}
.links {
  display: flex;
  align-items: center;
  gap: 80px;
  font-family: var(--font-btn), sans-serif;
  font-size: 16px;
  font-weight: 600;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 24px;
  font-family: var(--font-btn), sans-serif;
  font-size: 16px;
  font-weight: 600;
}
.signup {
  background: var(--color-accent);
  padding: 4px 18px;
  border-radius: 8px;
}
.signup:hover {
  background: var(--color-background-secondary);
}
.balance {
  display: flex;
  align-items: center;
  gap: 8px;
}
.balance .icon {
  color: var(--color-accent);
}
.username {
  text-decoration-line: underline;
  text-underline-offset: 3px;
}
</style>
