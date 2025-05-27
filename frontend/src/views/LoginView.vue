<script setup lang="ts">
import GoogleIcon from "@/components/icons/GoogleIcon.vue";
import GitHubIcon from "@/components/icons/GitHubIcon.vue";
</script>

<template>
  <div class="container">
    <div class="content">
      <div class="title">
        <router-link to="/">
          <h1>One<span>4</span>Lib</h1>
        </router-link>
        <h2>Log in</h2>
      </div>
      <div class="form-box">
        <form>
          <div class="input-group">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" placeholder="Type your email here" required />
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" placeholder="Type your password here" required />
          </div>
          <button type="submit" class="btn">Log in</button>
        </form>
        <div class="alternatively">
          <div class="separator">
            <hr>
            <span>Or Continue With</span>
            <hr>
          </div>
          <div class="social-buttons">
            <router-link to="/" class="google"><GoogleIcon height="38" width="38"/></router-link>
            <router-link to="/" class="github"><GitHubIcon height="38" width="38"/></router-link>
          </div>
        </div>
      </div>
      <div class="links">
        <router-link to="/signup">Don’t have an account? Sign up</router-link>
        <router-link to="/reset-password">Forgot your password?</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: radial-gradient(circle,var(--color-background-primary) 0%, var(--color-black) 100%);
}
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
}
.title {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.title h1 {
  font-size: 48px;
  font-weight: 275;
}
.title h1 span {
  color: var(--color-accent);
}
.title h1:hover span {
  color: var(--color-white);
}
.title h2 {
  font-size: 32px;
  font-weight: 275;
}
.form-box {
  width: 380px;
  background: linear-gradient(135deg, var(--color-background-primary), var(--color-black) 100%);
  padding: 30px;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  gap: 32px;
}
form {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.input-group {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 20px;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
}
.input-group label {
  margin-bottom: 2px;
}
.input-group input {
  padding: 8px 9px;
  border: 1px solid var(--color-placeholder-primary);
  border-radius: 6px;
  background: transparent;
}
.input-group input:focus {
  border-color: var(--color-accent);
  outline: none;
  color: var(--color-white);
}
.input-group input::placeholder {
  color: var(--color-placeholder-primary);
  font-family: 'Kulim Park', sans-serif;
}
.btn {
  margin-top: 10px;
}
.separator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
}
.separator hr {
  flex: 1;
  border: none;
  border-top: 1px solid var(--color-white);
}
.separator span {
  color: var(--color-white);
  line-height: 20px;
  font-size: 14px;
  font-weight: 400;
}
.alternatively {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
.links {
  display: flex;
  gap: 40px;
}
.links a{
  color: var(--color-white);
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  text-decoration-line: underline;
  text-underline-offset: 3px;
}
.social-buttons {
  display: flex;
  gap: 30px;
}
</style>
