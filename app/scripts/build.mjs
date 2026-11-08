/**
 * build.mjs — production build without the config loader.
 *
 * See dev-server.mjs for why `vite build` (which loads vite.config.js via a
 * piped child process) fails under the file sandbox. This passes the same
 * configuration inline instead.
 *
 * Usage:  node scripts/build.mjs
 */
import { build } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url)); // <repo>/app/scripts
const appRoot = resolve(here, '..'); // <repo>/app
const repoRoot = resolve(appRoot, '..'); // <repo>

await build({
  root: appRoot,
  configFile: false,
  plugins: [react()],
  publicDir: resolve(repoRoot, 'public'),
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    chunkSizeWarningLimit: 1200,
  },
  logLevel: 'info',
});

console.log('BUILD OK');
