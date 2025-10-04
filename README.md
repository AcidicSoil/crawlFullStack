# Full Stack Open (/en) Offline Markdown Mirror

This repo mirrors **<https://fullstackopen.com/en/>** to local Markdown for personal offline reference and programmatic reuse. It uses **crawl4ai** with strict safety guardrails.

## Safety & scope guardrails

- Single domain: `fullstackopen.com`, path prefix `/en/`.
- Robots honored. If disallowed the URL is skipped and logged.
- Concurrency ≤ 4 with jitter and exponential backoff on 429/5xx.
- Query traps and non-course assets pruned by allow/deny rules.
- Personal use only. Do not redistribute or publish mirrors.

## Install

This project uses `uv` for environment and dependency management.

```bash
# Create and activate a virtual environment
uv venv
source .venv/bin/activate

# Install dependencies in editable mode, including dev tools
uv pip install -e '.[dev]'

# Optional: Install Playwright browsers for JS-rendered pages
python -m playwright install chromium
```

## One-command runs

The `crawl` command is defined in `pyproject.toml`.

```bash
# Full fresh crawl + postprocess + linkcheck
uv run crawl --fresh

# Incremental since a date
uv run crawl --since 2025-01-01

# Dry run (no writes)
uv run crawl --dry-run

# Save raw HTML alongside Markdown
uv run crawl --save-html
```

## Code Quality

This project uses `ruff` for linting/formatting, `mypy` for type checking, and `bandit` for security scanning.

```bash
# Format code
ruff format .

# Lint for issues
ruff check .

# Type check
mypy .

# Run security scan
bandit -r .
```

## Layout

```md
fullstackopen-en-repo/
  README.md
  pyproject.toml
  crawl.config.yml
  seeds.txt
  .gitignore
  /.githooks/pre-commit
  /scripts/{crawl_fullstackopen.py, postprocess.py, linkcheck.py, utils_slug.py}
  /data/          # Markdown output, organized by part/section
  /assets/        # Downloaded images referenced by Markdown
  /logs/          # JSON Lines crawl and transform logs
```

## Refresh later

- Update `seeds.txt` if the course gains new parts.
- Re-run with `--since YYYY-MM-DD` to limit fetches.
- Deterministic queue: URLs sorted, stable slugging, normalized headings.

## Pre-commit hook

Enable the provided hook to block commits if linkcheck fails.

```bash
git config core.hooksPath .githooks
```

## License and use

Course content copyright to its owners. This mirror is **for personal use only**.
