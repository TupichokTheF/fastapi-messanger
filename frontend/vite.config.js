import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Dev-сервер проксирует /api (REST и WebSocket) на docker-бэкенд.
// docker-compose пробрасывает 1111:8000, поэтому на хосте бэкенд слушает 1111.
// changeOrigin + сохранение cookies обязательно для HttpOnly refresh_token.
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:1111',
        changeOrigin: true,
        ws: true,
      },
    },
  },
})
