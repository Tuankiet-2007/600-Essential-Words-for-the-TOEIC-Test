/**
 * verify_tabs.mjs — prove every tab renders against the REAL lesson data.
 *
 * Approach: bundle each tab (plus a tiny render harness) with Vite's own
 * rolldown/esbuild pipeline for the NODE platform, then execute the bundle and
 * server-render it. This avoids Vite's dev-mode SSR module runner, which
 * mishandles React's CJS build in this environment ("module is not defined").
 *
 * Catches crashes, null-lesson handling, and Context-First regressions
 * (a missing highlight/cloze shows up as a zero count).
 *
 * Usage:  node scripts/verify_tabs.mjs
 */
import { createServer, build } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, resolve } from 'node:path';
import { mkdtempSync, writeFileSync, readFileSync, readdirSync, mkdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { renderToString } from 'react-dom/server';
import React from 'react';

const here = dirname(fileURLToPath(import.meta.url));
const appRoot = resolve(here, '..');
const repoRoot = resolve(appRoot, '..');

const lesson = JSON.parse(
  readFileSync(resolve(repoRoot, 'public', 'lessons_json', 'lesson_01.json'), 'utf8'),
);
console.log(`lesson_01 loaded: ${lesson.words_to_learn.length} words\n`);

const TABS = [
  ['Tab1Vocabulary', 'src/tabs/Tab1Vocabulary.jsx'],
  ['Tab2Flashcards', 'src/tabs/Tab2Flashcards.jsx'],
  ['Tab3Srs', 'src/tabs/Tab3Srs.jsx'],
  ['Tab4AiLab', 'src/tabs/Tab4AiLab.jsx'],
  ['Tab5Practice', 'src/tabs/Tab5Practice.jsx'],
];

let pass = 0;
let fail = 0;
// Emit inside the app so bare imports like "react" resolve from app/node_modules.
const workDir = resolve(appRoot, '.tabrender');
mkdirSync(workDir, { recursive: true });

for (const [name, rel] of TABS) {
  // Entry re-exports the tab plus the provider, so the bundled tab resolves
  // its imports and can be rendered inside the real app context.
  const entry = resolve(workDir, `${name}.entry.jsx`);
  writeFileSync(
    entry,
    `export { default } from ${JSON.stringify(resolve(appRoot, rel).replace(/\\/g, '/'))};\n` +
      `export { AppProvider } from ${JSON.stringify(resolve(appRoot, 'src/lib/store.jsx').replace(/\\/g, '/'))};\n`,
  );

  const outDir = resolve(workDir, name);
  try {
    await build({
      root: appRoot,
      configFile: false,
      plugins: [react()],
      logLevel: 'silent',
      build: {
        lib: { entry, formats: ['es'], fileName: name },
        outDir,
        emptyOutDir: true,
        minify: false,
        ssr: true,
        rollupOptions: {
          // Keep React external so the bundle shares THIS process's React
          // instance. Bundling its own copy makes hooks see a null dispatcher
          // ("Cannot read properties of null (reading 'useContext')").
          external: ['react', 'react-dom', 'react-dom/server', 'react/jsx-runtime'],
        },
      },
      ssr: { noExternal: [], target: 'node' },
    });
  } catch (e) {
    fail++;
    console.log(`FAIL  ${name}: bundle error: ${String(e.message).slice(0, 220)}`);
    continue;
  }

  let mod;
  try {
    // Vite decides the emitted filename; discover it instead of assuming.
    const emitted = readdirSync(outDir).filter((f) => f.endsWith('.js'));
    if (!emitted.length) throw new Error(`no .js emitted into ${outDir}`);
    mod = await import(pathToFileURL(resolve(outDir, emitted[0])).href);
  } catch (e) {
    fail++;
    console.log(`FAIL  ${name}: bundle did not execute: ${String(e.message).slice(0, 220)}`);
    continue;
  }

  if (typeof mod.default !== 'function') {
    fail++;
    console.log(`FAIL  ${name}: default export is ${typeof mod.default}, expected function`);
    continue;
  }
  pass++;

  for (const [suffix, props] of [
    ['with lesson', { lesson }],
    ['lesson=null', { lesson: null }],
  ]) {
    try {
      // Tabs call useApp(), so they must render inside the real AppProvider.
      // The store fetches lesson data in an effect, which does not run during
      // SSR — harmless here; we are testing the render path, not the fetch.
      const html = renderToString(
        React.createElement(mod.AppProvider, null, React.createElement(mod.default, props)),
      );
      const hits = (html.match(/vocab-hit/g) || []).length;
      const blanks = (html.match(/_{4,}/g) || []).length;
      const vi = /[àáảãạăâđêôơư]/i.test(html);
      console.log(
        `PASS  ${name.padEnd(15)} ${suffix.padEnd(12)} html=${String(html.length).padStart(6)}B  highlight-marks=${String(hits).padStart(3)}  cloze-blanks=${String(blanks).padStart(3)}  vi-copy=${vi}`,
      );
      pass++;
    } catch (e) {
      fail++;
      console.log(`FAIL  ${name} (${suffix}) threw: ${String(e.message).slice(0, 220)}`);
    }
  }
}

console.log(`\n${pass} passed, ${fail} failed`);
// Clean up the scratch bundle directory.
try {
  rmSync(workDir, { recursive: true, force: true });
} catch {
  /* best effort */
}
process.exit(fail === 0 ? 0 : 1);
