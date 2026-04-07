import { defineConfig } from 'astro/config';

export default defineConfig({
  build: {
    format: 'file',   // page.html (디렉토리 index.html 방식 대신)
  },
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },
});
