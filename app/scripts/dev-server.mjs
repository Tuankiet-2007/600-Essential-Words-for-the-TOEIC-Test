/**
 * dev-server.mjs — start Vite programmatically, bypassing the config loader.
 *
 * WHY: `npm run dev` / `npm run build` fail in sandboxed sessions with
 *   [plugin externalize-deps] Error: spawn EPERM
 * because Vite 8's `loadConfigFromFile` bundles vite.config.js through
 * `bundleConfigFile` -> `windowsSafeRealPathSync` -> `child_process.exec`,
 * and exec uses piped stdio, which confined sessions block.
 *
 * Passing the config inline with `configFile: false` skips that code path
 * entirely, so the same config values are used without spawning anything.
 *
 * Usage:  node scripts/dev-server.mjs [port]
 */
import { createServer } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url)); // <repo>/app/scripts
const appRoot = resolve(here, '..'); // <repo>/app
const repoRoot = resolve(appRoot, '..'); // <repo>
const port = Number(process.argv[2] || 5173);

const server = await createServer({
  root: appRoot,
  configFile: false,
  plugins: [react()],
  publicDir: resolve(repoRoot, 'public'),
  server: {
    port,
    strictPort: false,
    host: '127.0.0.1',
    fs: { allow: [repoRoot] },
  },
  logLevel: 'info',
});

await server.listen();
const addr = server.httpServer?.address();
const actual = typeof addr === 'object' && addr ? addr.port : port;
server.printUrls();
console.log(`\n[dev-server] READY http://127.0.0.1:${actual}`);
