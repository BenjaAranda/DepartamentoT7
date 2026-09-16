import { copyFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/postcss';
import { defineConfig } from 'vite';

const web = dirname(fileURLToPath(import.meta.url));
const output = resolve(web, 'dist-static');
const base = process.env.T7_BASE_PATH || '/DepartamentoT7/';
if (!/^\/(?:[a-zA-Z0-9_-]+\/)*$/.test(base)) throw new Error('Invalid public base path');

export default defineConfig({
  root: resolve(web, 'static'),
  base,
  publicDir: false,
  resolve: { alias: { '@': web } },
  css: { postcss: { plugins: [tailwindcss()] } },
  plugins: [react(), {
    name: 't7-public-assets-allowlist',
    closeBundle() {
      for (const file of ['favicon.svg', 'reference/planta-t7.png', 'models/manifest.json',
        'models/departamento-t7-web.glb', 'models/departamento-t7.json']) {
        const target = resolve(output, file);
        mkdirSync(dirname(target), { recursive: true });
        copyFileSync(resolve(web, 'public', file), target);
      }
      writeFileSync(resolve(output, '.nojekyll'), '');
    },
  }],
  build: { outDir: output, emptyOutDir: true, sourcemap: false },
  preview: { host: '127.0.0.1', port: 4173, strictPort: true },
});
