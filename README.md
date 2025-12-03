# Full Stack Open (/en) Offline Markdown Mirror

This repo mirrors course content into Markdown using **crawl4ai** with strict safety guardrails. The crawler now supports multiple “site profiles,” including the original **Full Stack Open** and the new **Next.js Learn** curriculum at `https://nextjs.org/learn`.

## Motivation

The primary motivation for this project is to create a personal, offline-first copy of the excellent Full Stack Open curriculum. This allows for:

- **Offline Access:** Study the course material without an internet connection.
- **Local Search:** Use local search tools like `grep` or `ripgrep` to instantly find content across the entire course.
- **Programmatic Use:** Enables building other tools on top of the content, such as flashcard generators or concept extractors.
- **Long-Term Archive:** Preserves a personal copy of the course material.

## Features

- **Pluggable site profiles:** Scope, normalization, selectors, and output paths are encapsulated per site; `fullstackopen` and `nextjs-learn` ship in-tree with room for additional YAML-defined profiles later.
- **Web crawling via Crawl4AI:** Headless browsing + markdown extraction with configurable CSS selectors.
- **Markdown conversion + assets:** HTML → Markdown with local image downloads into a deterministic `assets/` directory.
- **Optional link rewriting:** `--rewrite-links local` converts internal URLs to relative paths; `--rewrite-links none` (default) preserves the source URLs.
- **Link validation + postprocess:** Shared link logic powers the crawler, postprocessor, and link checker, preventing drift.
- **Testing + safety:** Pytest suites cover profiles/link rewriting, and the crawler honors robots.txt while constraining depth/hostnames.

## Install

Create an isolated environment (venv, uv, or hatch all work). Vanilla `venv` instructions:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'

# Optional: install Playwright’s bundled Chromium for better JS rendering
python -m playwright install chromium
```

On Debian-based systems without `ensurepip`, install the `python3-full` package or fall back to `python3 -m pip install --user -e '.[dev]'`.

## How to use

The Typer CLI is exposed as `crawl` via `pyproject.toml`. Key flags:

```bash
# Crawl Full Stack Open (default site) without rewriting links
crawl --site fullstackopen --rewrite-links none

# Crawl Next.js Learn and rewrite internal links to relative .md files
crawl --site nextjs-learn --rewrite-links local --depth-limit 5

# Dry run (no writes) for planning
crawl --site fullstackopen --dry-run

# Persist HTML alongside markdown for debugging
crawl --save-html
```

Both the postprocess and linkcheck helpers accept the same knobs:

```bash
python -m fullstackopen_en_repo.postprocess --site nextjs-learn --rewrite-links local
python -m fullstackopen_en_repo.linkcheck --site nextjs-learn
```

Typical workflow:

1. **Crawl** the desired site profile, optionally saving HTML:

   ```bash
   crawl --site fullstackopen --rewrite-links none
   crawl --site nextjs-learn --rewrite-links local --save-html
   ```

2. **Postprocess** to switch link rewrite modes or rebuild `index.json` without re-crawling:

   ```bash
   python -m fullstackopen_en_repo.postprocess --site nextjs-learn --rewrite-links local
   ```

3. **Linkcheck** to ensure local references resolve:

   ```bash
   python -m fullstackopen_en_repo.linkcheck --site nextjs-learn
   ```

Link rewriting is always optional. Markdown is first stored exactly as Crawl4AI produced it; postprocess can be re-run later with a different mode if needed.

> **Tip:** Re-running `crawl` now skips writing pages whose stored checksum matches the freshly scraped content, so repeated runs won't duplicate data. Pass `--fresh` if you need to rewrite everything regardless.

Need alternate frontmatter? Pass `--frontmatter-template simple` to emit the YAML style from `frontmatter-example.txt` (with `id`/`title` fields plus metadata), otherwise the default JSON metadata block is used.

## Code Quality & Tests

Static analysis:

```bash
ruff format .
ruff check .
mypy .
bandit -r .
```

Unit tests exercise the profile + link rewriting logic:

```bash
pytest
```

## Project Structure

```
fullstackopen-en-repo/
├── assets/                # Downloaded images
├── data/                  # Markdown output tree (per site profile)
├── docs/                  # Aux docs / agent briefs
├── .githooks/pre-commit   # Optional linkcheck hook
├── src/fullstackopen_en_repo/
│   ├── crawl_fullstackopen.py   # Typer CLI entry point
│   ├── indexing.py              # index.json builder
│   ├── link_rewriter.py         # shared Markdown link mutator
│   ├── markdown_utils.py        # helpers for frontmatter parsing
│   ├── linkcheck.py             # CLI link validator
│   ├── postprocess.py           # CLI to re-run link rewriting / index
│   ├── profiles/
│   │   ├── base.py              # SiteProfile abstraction
│   │   ├── config_profile.py    # YAML-driven profile implementation
│   │   ├── fullstackopen.py     # Legacy mapping
│   │   └── nextjs_learn.py      # Next.js Learn site profile
│   └── utils_slug.py
├── tests/                # Pytest suites for profiles/link rewriting
├── crawl.config.yml      # Generic crawl knobs (UA, timeouts, selectors)
├── pyproject.toml        # Dependencies + CLI entry point
└── README.md
```

## Refresh later

- Update or add site profiles (YAML or Python) when targeting new courses.
- Re-run with `--since YYYY-MM-DD` once incremental crawling support is implemented.
- Deterministic queue: URLs sorted, normalized headings, and slugged filenames keep diffs readable.

## Pre-commit hook

Enable the provided hook to block commits if linkcheck fails.

```bash
git config core.hooksPath .githooks
```

## License and use

Course content copyright to its owners. This mirror is **for personal use only**.
