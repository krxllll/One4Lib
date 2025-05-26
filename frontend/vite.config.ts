import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  base: './',
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    host: '0.0.0.0',
    watch: {
      usePolling: true,
      interval: 100,
    },
    hmr: {
      host: 'localhost',
      protocol: 'ws',
      port: 3000,
    },
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/openapi.json': {
        target: 'http://backend:8000/openapi.json',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/openapi.json/, ''),
      },
    },
  },
  build: {
    outDir: 'dist',
  },
})
