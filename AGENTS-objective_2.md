Handoff spec: generalize crawler and add optional link rewriting

---

Objective
Refactor the existing Fullstack Open–specific crawler into a site-agnostic engine with pluggable “site profiles,” and add a CLI-controlled link rewriting mode:

```md
a CLI flag:

--rewrite-links local vs --rewrite-links none
```

`--rewrite-links none` must be the default behavior.

---

1. Architecture split

Create a clean separation between:

1. Core engine

- BFS queue and depth handling
- Crawl4AI integration (HTTP fetch, HTML → markdown)
- Asset download and checksum
- Index generation (`index.json`, etc.)

2. SiteProfile abstraction

- Scope rules (which URLs are in/out)
- URL normalization
- Output path mapping (URL → local markdown path)
- Link classification (internal vs external)
- Optional content extraction selectors

3. Optional link rewriting layer

- Operates on markdown after Crawl4AI output
- Reads the `--rewrite-links` mode
- Uses `SiteProfile` to map internal URLs to local paths

Engine code must be unaware of any specific site (Fullstack Open, Next.js Learn, etc.); it only talks to `SiteProfile` and the link rewriting layer.

---

2. SiteProfile interface

Implement a `SiteProfile` interface with at least:

Identity

- `id: str`
- `domains: list[str]`
- `entrypoints: list[str]`  # default seeds
- `default_max_depth: int`

Scope and normalization

- `normalize_url(url: str) -> str`

  - Canonicalize scheme/host
  - Strip query and fragment as appropriate
- `in_scope(url: str) -> bool`

  - Domain ∈ `domains`
  - Path matches allow/deny rules
- `should_enqueue(url: str) -> bool`

  - Typically `in_scope(url)` plus optional constraints (file type, path patterns, etc.)

Output mapping

- `output_root: Path`
- `derive_output_path(url: str) -> Path`

  - Deterministic URL → markdown path under `output_root`

Link handling

- `is_internal_link(href: str) -> bool`

  - Decide if `href` points to something controlled by this profile
- `to_absolute(href: str, from_url: str) -> str`

  - Resolve relative hrefs against `from_url`
- (used only when rewriting) `map_url_to_relpath(from_url: str, target_url: str) -> str`

  - Compute relative path between `derive_output_path(from_url)` and `derive_output_path(target_url)`

Content extraction (optional, but recommended)

- `content_selectors: list[str]`  # CSS/XPath to keep
- `remove_selectors: list[str]`   # CSS/XPath to drop (nav, footer, ads)

---

3. Config-driven profiles

Avoid writing custom Python per site where possible. Implement a generic `ConfigSiteProfile` that can be constructed from a YAML/JSON config.

Config schema (example):

```yaml
id: "nextjs-learn"
domains: ["nextjs.org"]
entrypoints:
  - "https://nextjs.org/learn"
default_max_depth: 4

scope:
  allow:
    - "^/learn(/.*)?$"
  deny:
    - "\\.(png|jpe?g|gif|svg|pdf)$"
  strip_query: true
  strip_fragment: true

content:
  keep:
    - "main"
    - "article"
  remove:
    - "header"
    - "nav"
    - "footer"

output:
  base_dir: "data/nextjs-learn"
  index_for_dirs: true
  pattern: "{path_segments}"

links:
  internal:
    - "^https?://(www\\.)?nextjs\\.org/learn(/.*)?$"
    - "^/learn(/.*)?$"
```

`ConfigSiteProfile` responsibilities:

- Compile `scope.allow/deny` into regex checks for `in_scope` and `should_enqueue`.
- Use `strip_query/strip_fragment` in `normalize_url`.
- Use `output.*` to implement `derive_output_path`.
- Use `links.internal` to implement `is_internal_link`.

Provide at least two concrete profiles:

- `FullstackOpenProfile` (can be config + small code) that preserves existing behavior.
- `NextjsLearnProfile` built via config as above.

---

4. URL → file mapping (output patterns)

Replace hardcoded path logic with a reusable mapping mechanism.

Implement simple mapping rules:

- Parse URL:

  - `path` = `/a/b/c` (no query/fragment)
  - `segments` = `["a", "b", "c"]`
- Options:

  - `index_for_dirs: bool`

    - If `true`:

      - `[]` → `index.md`
      - `["learn"]` → `learn/index.md`
      - `["learn", "dashboard-app"]` → `learn/dashboard-app/index.md`
      - `["learn", "dashboard-app", "getting-started"]` → `learn/dashboard-app/getting-started.md`
  - `index_for_dirs: false`:

    - `["docs"]` → `docs.md`
    - `["docs", "getting-started"]` → `docs/getting-started.md`

Slugging:

- URL-decode segments.
- Replace characters invalid for filenames with `-`.
- Lowercasing is acceptable but must be consistent.

`derive_output_path(url)` combines `output_root` + the mapped relative path.

---

5. Link rewriting modes (CLI flag)

Add a global CLI flag that controls link rewriting:

```md
a CLI flag:

--rewrite-links local vs --rewrite-links none
```

Behavior:

- Default = `--rewrite-links none`.
- Engine always stores markdown with the links produced by Crawl4AI (original URLs) before any optional rewriting.

Implement a link rewriting module:

- Input:

  - `mode: Literal["none", "local"]`
  - `profile: SiteProfile`
  - `from_url: str`
  - markdown text
- For `mode == "none"`:

  - Return markdown unchanged.
- For `mode == "local"`:

  - Parse markdown links `[text](href)`
  - Resolve `href` to absolute with `profile.to_absolute(href, from_url)`
  - If not `profile.is_internal_link(abs_url)`:

    - Leave `href` unchanged (remain as absolute or relative external links).
  - If internal:

    - `relpath = profile.map_url_to_relpath(from_url, abs_url)`
    - Replace `href` with `relpath`.

The rewriting module must be the single place where link rewriting is implemented. No other code or script may hardcode regex-based URL → path conversions.

---

6. Integration points

Crawler main loop

- At startup:

  - Parse CLI flags including `--site` and `--rewrite-links`.
  - `profile = load_profile(site_name)` (using config/registry).
- Seeds:

  - `queue` initialized with `profile.entrypoints`.
- For each URL:

  - Normalize via `profile.normalize_url`.
  - Skip if `not profile.in_scope(url)`.
- When fetching and rendering markdown:

  - Let Crawl4AI produce markdown and links normally.
  - Pass markdown through the link rewriting module with the selected `mode` before writing to disk.
  - Use `profile.derive_output_path(url)` to decide file path.

Postprocess script

- Accept the same `--site` and `--rewrite-links` flags.
- Load the same `profile`.
- If the script needs to adjust links again (should be rare), it must call the same link rewriting module with the chosen `mode`.
- If its job is only to rebuild an index or add metadata, it must not touch links at all.

Linkcheck script

- Accept the same `--site`.
- Load `profile`.
- Read markdown files and interpret links:

  - Use `profile.is_internal_link` on URLs reconstructed from the current markdown paths if needed.
  - For internal links, verify that the target file exists (according to `derive_output_path`).
- Do not perform any rewriting; linkcheck is read-only.

---

7. Profile loader and registry

Implement:

- `load_profile(name: str) -> SiteProfile`

Mechanism:

- Scan a `profiles/` directory for YAML files.
- Map profile id to config.
- Build `ConfigSiteProfile` instances.
- Allow hard-coded overrides when necessary (e.g., if a site requires custom extraction code beyond config).

CLI options:

- `--site fullstackopen`
- `--site nextjs-learn`
- Future: other site IDs.

---

8. Backward compatibility for Fullstack Open

For the `fullstackopen` profile:

- Replicate current URL scope and output layout.
- Ensure that running with `--site fullstackopen --rewrite-links local` reproduces the previous relative-link behavior (or as close as possible).
- With `--rewrite-links none`, it must generate artifacts that retain the original absolute URLs (no “cut” links).

If necessary:

- Keep the old mapping rules inside `FullstackOpenProfile`’s `derive_output_path` and `map_url_to_relpath`, but do not expose them anywhere else.

---

9. Minimal tests

Add tests that cover:

- `ConfigSiteProfile` created from a sample YAML:

  - `normalize_url`, `in_scope`, `should_enqueue`.
  - `derive_output_path` mapping examples.
- Link rewriting module:

  - `mode == "none"`: markdown unchanged.
  - `mode == "local"`:

    - Internal absolute URLs → correct relative paths.
    - Internal root-relative URLs → correct relative paths.
    - External URLs → unchanged.
- Smoke test:

  - Run a tiny in-memory crawl (or file-backed fixture) with both `--rewrite-links none` and `--rewrite-links local` and assert that:

    - Files are written to expected paths.
    - Link forms differ according to mode, but content bodies are otherwise identical.
