# 23 November 2026: Rescuers pull a boy alive from the rubble in Dymer

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Reki120/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Reki120/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

An entry for the make.fun bounty [news-image-20261123](https://make.fun/bounty/news-image-20261123): sum up the world's news of Monday 23 November 2026 in one image. The entry is drawn as a newspaper front page, with the date across the top so the day it sums up is unmistakable.

## The day's news, as the image tells it

- **Lead — Dymer, Ukraine.** A Russian strike levelled an apartment block in Dymer, north of Kyiv. The main scene shows the night rescue: a standing wall of the block with one window still lit, fallen floor slabs and a rubble mound, and rescuers in helmets and hi-vis vests digging under headlamp beams. At the centre a rescuer carries out a 7-year-old boy wrapped in a blue blanket, pulled out alive while the death toll climbed past 15.
- **Benghazi, Libya.** A Russian navy corvette sank at Benghazi naval base after a suspected Ukrainian sea-drone strike — the panel shows the grey corvette settling by the stern, smoke rising, with the small dark shape of a sea drone closing in across the water.
- **Antalya, Türkiye.** The COP31 climate talks collapsed without a deal — a torn agreement hangs over a conference table of empty chairs, one of them tipped over.
- **Strait of Hormuz.** Two supertankers ablaze near the strait — black tanker silhouettes under an orange dusk sky, flames and smoke rising, the rocky shores of the strait closing in at both corners.

## How it works

- `entry.png` is the entry image (1024 × 1024 PNG, well under the 1 MiB cap).
- `draw_entry.py` is the authoring source: a Python PIL program that draws the whole front page — banner, headline, lead scene and the three side panels — in flat shapes and bold text. Re-running it reproduces `entry.png`.
- `main.ts` is the entered program (Node 22, standard library only, no network). It copies the committed `entry.png` to `/output/entry.png`, then reads the copy back and compares it byte for byte with the source, failing loudly on any mismatch — so the two grader runs always write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
