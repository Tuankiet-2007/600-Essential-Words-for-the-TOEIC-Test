import fs from 'node:fs';
import { makeCloze } from './src/lib/assets.js';
const lesson = JSON.parse(fs.readFileSync('.lesson.json','utf8'));
const html = fs.readFileSync('.ssr/tab2.html','utf8');
console.log('html file?', html.length);
