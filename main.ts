// news-image-20261123: "Sum up 23 November's world news in one image".
//
// The entry image lives in this repository as entry.png (drawn by
// draw_entry.py, which stays in the repo as its authoring source). This
// program copies that file to the output directory as entry.png and then
// reads the copy back and compares it byte for byte with the source, so a
// short or corrupted write fails loudly instead of entering a broken image.
//
// Node 22, standard library only, no network. Outside the grader's
// container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from "node:crypto";
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const sourcePath = new URL("./entry.png", import.meta.url);
const targetPath = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(sourcePath, targetPath);

const expected: Buffer = readFileSync(sourcePath);
const written: Buffer = readFileSync(targetPath);
if (written.length !== expected.length || !written.equals(expected)) {
  throw new Error(
    `entry.png verification failed: wrote ${written.length} bytes, source holds ${expected.length}`,
  );
}
const digest = createHash("sha256").update(written).digest("hex");
console.log(`entry.png copied to ${targetPath} (${written.length} bytes, verified identical)`);
console.log(`sha256: ${digest}`);
