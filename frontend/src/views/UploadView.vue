<script setup lang="ts">
import PointIcon from "@/components/icons/PointIcon.vue";
import FolderIcon from "@/components/icons/FolderIcon.vue";
import {ref, watch} from 'vue'
import { type FileType, fileTypes } from "@/types/file.ts";
import { api } from "@/utils/api.ts";
import { useAuthStore } from "@/stores/auth.ts";
import { handleApiError } from "@/utils/handleApiError.ts";

const auth = useAuthStore();

const file = ref<File | null>(null)
const fileName = ref('')
const isDragOver = ref(false)

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const selected = target.files?.[0] || null
  if (selected) {
    file.value = selected
    fileName.value = selected.name
  }
}

function onDragOver() {
  isDragOver.value = true
}

function onDragLeave() {
  isDragOver.value = false
}

function onDrop(event: DragEvent) {
  isDragOver.value = false
  const selected = event.dataTransfer?.files?.[0]
  if (selected) {
    file.value = selected
    fileName.value = selected.name
  }
}

const fileTitle = ref('')
const fileDescription = ref('')
const fileType = ref<FileType>()
const filePrice = ref(0)

watch(fileName, () => {
  if (fileName.value) {
    const fileExtension = fileName.value.split('.').pop()?.toLowerCase()
    if (fileExtension) {
      const type = fileTypes.find(t => t.toLowerCase().split('/')[1] === fileExtension)
      fileType.value = type ? type : undefined
    } else {
      fileType.value = undefined
    }
  } else {
    fileType.value = undefined
  }
})

async function uploadFile() {
  if (!fileType.value) {
    alert('Unsupported file type. Please upload a PNG, PDF, or MP3 file.')
    return
  }
  if (!file.value || !fileTitle.value || !fileDescription.value || filePrice.value < 0) {
    alert('Please fill in all fields and select a file.')
    return
  }

  const meta = {
    title: fileTitle.value,
    description: fileDescription.value,
    file_type: fileType.value,
    price: filePrice.value,
  }

  const formData = new FormData()
  formData.append('meta', JSON.stringify(meta))
  formData.append('raw_file', file.value!)

  try {
    const response = await api.post('/files/upload', formData)
    console.log('File uploaded successfully:', response)
    alert('File uploaded successfully!')
    await auth.getUserBalance()
    fileName.value = ''
    fileTitle.value = ''
    fileDescription.value = ''
    filePrice.value = 0
    file.value = null
  } catch (err) {
    const message = handleApiError(err, 'File upload failed')
    console.error('File upload error:', message)
  }
}
</script>

<template>
  <main class="container">
    <div class="title">
      <h1>Upload your file here</h1>
      <p>Currently supported filetypes: PNG, PDF, MP3</p>
    </div>
    <form class="content" @submit.prevent="uploadFile">
      <div class="upload-form">
        <div class="input-group">
          <label for="title">Title</label>
          <input v-model="fileTitle" type="text" id="title" placeholder="Type file title" required />
        </div>
        <div class="input-group">
          <label for="description">Description</label>
          <textarea v-model="fileDescription" id="description" placeholder="Type file description" />
        </div>
        <div class="input-group">
          <label for="price">Price</label>
          <div class="price">
            <input v-model="filePrice" type="number" id="price" placeholder="Type file price" required />
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
          <input type="file" accept=".png, .pdf, .mp3" name="file" @change="onFileChange" />
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
  font-family: var(--font-btn), sans-serif;
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
  font-family: var(--font-primary), sans-serif;
}
.input-group input:focus, .input-group textarea:focus {
  border-color: var(--color-accent);
  outline: none;
  color: var(--color-white);
}
.input-group input::placeholder, .input-group textarea::placeholder {
  color: var(--color-placeholder-primary);
  font-family: var(--font-primary), sans-serif;
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
