<script setup lang="ts">

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
    </div>
    <div class="user-info">
      <router-link to="/login">Login</router-link>
      <router-link to="/signup" class="signup">Sign Up</router-link>
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
}
.logo {
  font-size: 24px;
  font-weight: 275;
}
.logo span {
  color: var(--color-accent);
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
  background: color-mix(in srgb, var(--color-accent) 65%, transparent);
  padding: 4px 18px;
  border-radius: 8px;
}
</style>
