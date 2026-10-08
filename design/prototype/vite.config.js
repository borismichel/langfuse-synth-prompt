import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import { fileURLToPath } from 'node:url';
const local = p => fileURLToPath(new URL(p, import.meta.url));
export default defineConfig({
  plugins: [tailwindcss()],
  esbuild: {jsx: 'automatic'},
  resolve: {alias: {'@/src': local('./vendor/langfuse/web/src'), 'next/link': local('./src/Link.tsx')}},
  server: {strictPort: true}
});
