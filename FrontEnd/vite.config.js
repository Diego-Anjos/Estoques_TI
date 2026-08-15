import { defineConfig } from 'vite';
import { resolve, relative, sep } from 'node:path';
import { readdirSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const rootDir = fileURLToPath(new URL('.', import.meta.url));

/**
 * Descobre todos os index.html em `pages/` (MPA) + o index.html da raiz.
 */
function collectHtmlInputs() {
  const inputs = {
    main: resolve(rootDir, 'index.html'),
  };

  function walk(dir) {
    for (const name of readdirSync(dir)) {
      const full = resolve(dir, name);
      if (statSync(full).isDirectory()) {
        walk(full);
        continue;
      }
      if (name !== 'index.html') continue;

      const rel = relative(rootDir, full).split(sep).join('/');
      // chave estável: pages/auth/login/index.html → pages-auth-login
      const key = rel
        .replace(/\/index\.html$/i, '')
        .replace(/[^\w]+/g, '-')
        .replace(/^-|-$/g, '');
      inputs[key || 'page'] = full;
    }
  }

  walk(resolve(rootDir, 'pages'));
  return inputs;
}

export default defineConfig({
  // Caminhos absolutos a partir da raiz do site (necessário em páginas aninhadas na Vercel)
  base: '/',
  root: rootDir,
  publicDir: 'public',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    assetsDir: 'assets',
    rollupOptions: {
      input: collectHtmlInputs(),
    },
  },
  server: {
    port: 5173,
    open: '/pages/auth/login/index.html',
  },
  preview: {
    port: 4173,
  },
});
