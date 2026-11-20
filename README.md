# news-image-20261120-entry

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/rezimtirani/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/rezimtirani/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up the world's news of Friday 20 November 2026, drawn as a
newspaper front page: Cyclone Akvan comes ashore in Odisha, Trump says he is in
no rush over Iran, the UN court finds Myanmar guilty of genocide, Europe opens
up to talks with Russia, and a missile hits Riyadh's PIF Tower — plus four
shorter stories from the day.

## How it is built

- `news.json` — the day's stories, researched from Reuters, AP, BBC and
  The Hindu reporting of 20 November 2026.
- `render.py` — draws the front page with Pillow (DejaVu fonts) into
  `entry.png`, a 1024×1024 PNG. Fully offline and deterministic.
- `main.py` — the entrypoint: it copies the checked `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the PNG header and size
  limits (≤1024×1024, ≤1 MiB). Standard library only.

## Run it

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=pardomuan-kasudungan&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
