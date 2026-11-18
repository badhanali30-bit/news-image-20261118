// Copy entry.png into the make.fun output directory.
//
// Usage: MAKEFUN_OUTPUT_DIR=out node main.ts
// If MAKEFUN_OUTPUT_DIR is unset, /output is used.
// Standard library only; copies the file byte-for-byte.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(source, dest);
console.log(`copied entry.png -> ${dest}`);
