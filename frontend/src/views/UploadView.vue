<script setup lang="ts">
import PointIcon from "@/components/icons/PointIcon.vue";
import FolderIcon from "@/components/icons/FolderIcon.vue";
import { ref } from 'vue'

const fileName = ref('')
const isDragOver = ref(false)

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) fileName.value = file.name
}

function onDragOver() {
  isDragOver.value = true
}

function onDragLeave() {
  isDragOver.value = false
}

function onDrop(event: DragEvent) {
  isDragOver.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) fileName.value = file.name
}
</script>

<template>
  <main class="container">
    <div class="title">
      <h1>Upload your file here</h1>
      <p>Currently supported filetypes: PNG, PDF, MP3</p>
    </div>
    <form class="content">
      <div class="upload-form">
        <div class="input-group">
          <label for="title">Title</label>
          <input type="text" id="title" placeholder="Type file title" required />
        </div>
        <div class="input-group">
          <label for="description">Description</label>
          <textarea id="description" placeholder="Type file description" />
        </div>
        <div class="input-group">
          <label for="price">Price</label>
          <div class="price">
            <input type="number" id="price" placeholder="Type file price" required />
            <PointIcon height="24" width="24" viewBox="0 0 24 24" class="icon" />
          </div>
        </div>
        <button type="submit" class="btn">Upload</button>
      </div>
      <div class="upload-box"
           @dragover.prevent="onDragOver"
           @dragleave="onDragLeave"
           @drop.prevent="onDrop"
           :class="{ 'drag-over': isDragOver }"
      >
        <FolderIcon height="64" width="64" viewBox="0 0 512 512" class="icon" />
        <p>Drag and drop your file here</p>
        <label class="file-upload btn">
          <input type="file" accept=".png, .pdf, .mp3" @change="onFileChange" required />
          <span>{{ fileName || 'Choose file' }}</span>
        </label>
      </div>
    </form>
  </main>
</template>

<style scoped>
.container {
  padding-top: 16px;
  padding-bottom: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 32px;
  height: calc(100vh - 71px);
  background-color: var(--color-background-primary);
}
.title {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  border-bottom: 2px solid var(--color-background-secondary);
  padding-bottom: 32px;
}
.content {
  display: flex;
  gap: 64px;
  width: 100%;
}
.upload-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 40%;
}
.upload-box {
  flex: 1;
  border: 2px dashed var(--color-background-secondary);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 32px;
}
.upload-box .icon {
  color: var(--color-background-secondary);
}
.upload-box:hover .icon, .upload-box.drag-over .icon {
  color: var(--color-accent);
}
.upload-box p {
  color: var(--color-white);
  font-size: 16px;
  font-weight: 400;
}
.upload-box:hover, .upload-box.drag-over {
  border: 2px dashed var(--color-accent);
}
.input-group {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: 600;
  line-height: 20px;
}
.input-group label {
  margin-bottom: 8px;
}
.input-group textarea {
  resize: vertical;
  height: 200px;
  width: 100%;
  max-height: 375px;
  min-height: 80px;
}
#price {
  width: 30%;
}
.input-group .price {
  display: flex;
  align-items: center;
  gap: 8px;
}
.input-group .price .icon {
  color: var(--color-accent);
}
.input-group input, .input-group textarea {
  padding: 8px 9px;
  border: 1px solid var(--color-placeholder-primary);
  border-radius: 6px;
  background: transparent;
  font-size: 16px;
  color: var(--color-white);
}
.input-group input:focus, .input-group textarea:focus {
  border-color: var(--color-accent);
  outline: none;
  color: var(--color-white);
}
.input-group input::placeholder, .input-group textarea::placeholder {
  color: var(--color-placeholder-primary);
  font-family: 'Kulim Park', sans-serif;
}
.file-upload input[type="file"] {
  display: none;
}
.file-upload {
  display: flex;
  align-items: center;
  justify-content: center;
  width: auto;
  height: auto;
  padding: 8px 16px;
}
.file-upload span {
  line-height: 30px;
  font-size: 16px;
  font-weight: 600;
}
</style>
