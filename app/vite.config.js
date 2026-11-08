import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Assets (audio/, part1_photos/, sample_lessons/, lessons_json/) live in the
// REPO ROOT, one level above this app/ folder. Point Vite's publicDir at the
// root so URLs resolve as /audio/track_01.mp3 and /sample_lessons/lesson_01.json.
export default defineConfig({
  base: './',
  plugins: [react()],
  publicDir: '../public',
  server: {
    port: 5173,
    strictPort: false,
    fs: {
      // Allow serving files from the repo root during dev.
      allow: ['..'],
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    chunkSizeWarningLimit: 1200,
  },
})
