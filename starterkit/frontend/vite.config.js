import { fileURLToPath, URL } from "node:url"
import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"

// Keep VITE_PORT in sync with DJANGO_VITE_DEV_SERVER_PORT when changing it.
const port = Number(process.env.VITE_PORT ?? 5173)

export default defineConfig({
  plugins: [vue()],
  // Django serves built assets under STATIC_URL; django-vite requests dev assets from the same path.
  base: "/static/",
  resolve: {
    alias: {
      "@": fileURLToPath(new URL(".", import.meta.url)),
    },
  },
  server: {
    host: "localhost",
    port,
    strictPort: true,
    // Asset URLs (e.g. imported images) point at the Vite server, not Django.
    origin: `http://localhost:${port}`,
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
    manifest: "manifest.json",
    rollupOptions: {
      input: fileURLToPath(new URL("./app.js", import.meta.url)),
    },
  },
})
