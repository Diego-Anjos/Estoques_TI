import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 5173,
    open: '/pages/auth/login/index.html',
  },
  preview: {
    port: 4173,
  },
});
