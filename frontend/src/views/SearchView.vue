<script setup lang="ts">
import { onMounted, ref, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import { api } from "@/utils/api.ts";
import FilterIcon from "@/components/icons/FilterIcon.vue";
import SearchIcon from "@/components/icons/SearchIcon.vue";
import FileThumbnail from "@/components/FileThumbnail.vue";
import { handleApiError } from "@/utils/handleApiError.ts";
import { type File, fileTypes, type FileType, fileTypeColors } from "@/types/file.ts";

const selectedTypes = ref<FileType[]>([])

const isSelected = (type: FileType): boolean => selectedTypes.value.includes(type)

const getColorClass = (type: FileType): string => {
  const t = type.toLowerCase().split('/')[0]
  return fileTypeColors[t] || 'unselected'
}

const selectAll = () => {
  selectedTypes.value = [...fileTypes]
}

const deselectAll = () => {
  selectedTypes.value = []
}

const toggleFilters = () => {
  const filtersButton = document.querySelector('.filters') as HTMLButtonElement;
  if (filtersButton) {
    filtersButton.classList.toggle('active');
  }
  // Additional logic for toggling filters can be added here
}

const files = ref<File[]>([])
const fileCount = computed(() => files.value.length)

async function getFiles() {
  try {
    const params: any = {}
    if (selectedTypes.value.length > 0 && selectedTypes.value.length < fileTypes.length) {
      params.file_type = selectedTypes.value
    }
    const { data } = await api.get('/files/', { params })
    files.value = data
    console.log('Files fetched successfully:', files.value)
    console.log('Selected types:', selectedTypes.value)
  } catch (err) {
    const message = handleApiError(err, 'Fetching files failed')
    console.error('Error while fetching files:', message)
  }
}

watch(selectedTypes, () => {
  getFiles()
})

onMounted(() => {
  getFiles()
})

const router = useRouter()
const goToDetails = (id: string) => {
  router.push({ name: 'fileDetails', params: { id } })
}
</script>

<template>
  <div class="container">
    <div class="filetypes">
      <div class="filetypes-list">
        <label
          v-for="type in fileTypes"
          :key="type"
          :class="['file-type-option', isSelected(type) ? getColorClass(type) : 'unselected']"
        >
          <input
            type="checkbox"
            style="display: none"
            :value="type"
            v-model="selectedTypes"
          >
          <span>{{ type.split('/')[1].toUpperCase() }}</span>
        </label>
      </div>
      <div class="select-buttons">
        <button @click="selectAll">Select all</button>
        <button @click="deselectAll">Deselect all</button>
      </div>
    </div>
    <div class="search">
      <div class="inputs">
        <div class="search-bar">
          <input type="search" placeholder="Search file by name" />
          <SearchIcon height="16" width="16" class="icon"/>
        </div>
        <div class="input-group">
          <input type="checkbox" id="affordable">
          <label for="affordable">I can afford</label>
        </div>
        <div class="input-group">
          <button class="filters" @click="toggleFilters">
            <FilterIcon height="16" width="16" class="icon"/>
            <span>Filters</span>
          </button>
        </div>
      </div>
      <div class="search-results">
        <h1>Search results: <span>{{ fileCount }}</span> were found</h1>
        <div class="results">
          <FileThumbnail
            v-for="file in files || []"
            :key=file.id :title=file.title
            :type=file.file_type
            :imageUrl=file.thumbnail_url
            @click="goToDetails(file.id)"
          />
        </div>
        <button class="btn">Load More</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  background-color: var(--color-black);
  padding-top: 16px;
  padding-bottom: 16px;
  gap: 40px;
  min-height: calc(100vh - 71px);
}
.filetypes {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.filetypes-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: linear-gradient(135deg, var(--color-background-primary) 0%, var(--color-black) 100%);
  border-radius: 32px;
  padding: 12px 16px;
}
.select-buttons {
  display: flex;
  gap: 40px;
}
.select-buttons button {
  background: none;
  border: none;
  color: var(--color-white);
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  text-decoration-line: underline;
  text-underline-offset: 3px;
  cursor: pointer;
}
.select-buttons button:hover {
  color: var(--color-accent);
}
.file-type-option {
  padding: 14px 18px;
  width: 160px;
  height: 40px;
  border-radius: 20px;
  border: none;
  display: flex;
  align-items: center;
  cursor: pointer;
}
.filetype span {
  font-size: 16px;
  font-weight: 400;
  color: #fff;
  font-family: var(--font-btn), sans-serif;
}
.search {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 16px;
}
.inputs {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 40px;
}
.search-bar {
  flex: 1;
  position: relative;
}
.search-bar .icon {
  position: absolute;
  top: 50%;
  left: 16px;
  transform: translateY(-50%);
  color: var(--color-placeholder-secondary);
  pointer-events: none;
}
.search-bar input {
  width: 100%;
  padding: 14px 40px;
  border-radius: 20px;
  background: linear-gradient(90deg, var(--color-background-primary) 0%, var(--color-black) 100%);
  color: var(--color-white);
  font-size: 16px;
  font-weight: 400;
  border: 1px solid var(--color-black);
  font-family: var(--font-primary), sans-serif;
}
.search-bar input::placeholder {
  font-size: 16px;
  font-weight: 400;
  font-family: var(--font-primary), sans-serif;
  color: var(--color-placeholder-secondary);
}
.search-bar input:focus {
  outline: none;
  border: 1px solid var(--color-accent);
}
.search-bar input:focus + .icon {
  color: var(--color-accent);
}
.input-group {
  display: flex;
  align-items: center;
  gap: 8px;
}
.input-group input {
  width: 16px;
  height: 16px;
  accent-color: var(--color-accent);
  cursor: pointer;
}
.input-group button {
  background: none;
  border: none;
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--color-white);
  cursor: pointer;
}
.input-group:hover, .input-group button:hover {
  color: var(--color-accent);
}
.input-group button.active .icon {
  color: var(--color-accent);
  fill: var(--color-accent);
}
.input-group span, .input-group label {
  font-size: 16px;
  font-weight: 400;
  font-family: var(--font-btn), sans-serif;
  cursor: pointer;
}
.search-results {
  display: flex;
  flex-direction: column;
  padding: 16px 40px;
  background: linear-gradient(180deg, var(--color-background-primary) 0%, rgba(0, 0, 0, 1) 100%);
  border-radius: 32px;
  gap: 32px;
  flex: 1;
}
.search-results h1 {
  font-size: 32px;
  font-weight: 200;
  color: var(--color-white);
}
.search-results h1 span {
  color: var(--color-accent);
  font-family: var(--font-btn), sans-serif;
}
.search-results .results {
  display: flex;
  flex-wrap: wrap;
  gap: 32px;
}
.btn {
  align-self: center;
}
</style>
