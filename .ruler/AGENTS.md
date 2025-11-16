# AGENTS.md

---

Objective
Adapt the existing crawler to target the Next.js Learn course and all of its children under `https://nextjs.org/learn`, using a clean, path-shaped output layout and correct internal link rewriting. ([Next.js][1])

---

1. Target site definition

Implement a dedicated site profile for Next.js Learn.

Profile name: `NextjsLearnProfile`

Constants:

* Domain: `nextjs.org`
* Path prefix: `/learn`
* Course root: `https://nextjs.org/learn` ([Next.js][1])
* Example child paths:

  * `https://nextjs.org/learn/dashboard-app` (course overview) ([Next.js][2])
  * `https://nextjs.org/learn/dashboard-app/getting-started` (chapter page) ([Next.js][3])

Scope rules:

* In scope if:

  * `url.hostname == "nextjs.org"` and
  * `url.path == "/learn"` or `url.path.startswith("/learn/")`
* Ignore query parameters and fragments for canonicalization (`?foo=bar`, `#section`).

---

2. Site profile interface

Implement `NextjsLearnProfile` to satisfy the following interface (match exact names if similar abstraction already exists):

* `name: str = "nextjs-learn"`
* `domains: list[str] = ["nextjs.org"]`
* `start_urls: list[str] = ["https://nextjs.org/learn"]`
* `max_depth: int`

  * Set to a value sufficient to traverse:

    * `/learn`
    * course overview pages like `/learn/dashboard-app`
    * all chapter pages like `/learn/dashboard-app/getting-started`, `/learn/dashboard-app/css-styling`, etc. ([Next.js][3])

Methods:

1. `normalize_url(url: str) -> str`

   * Strip fragments (`#...`) and query strings (`?...`).
   * Convert scheme + host to canonical form (`https://nextjs.org/...`).
   * Ensure trailing slashes are normalized:

     * Prefer no trailing slash except for `/learn`.

2. `in_scope(url: str) -> bool`

   * Parse URL.
   * Return `True` iff:

     * `hostname == "nextjs.org"`
     * `path == "/learn"` or `path.startswith("/learn/")`

3. `should_enqueue(url: str) -> bool`

   * Return `True` iff `in_scope(url)` is `True`.
   * This allows BFS to follow all children under `/learn`, including:

     * `/learn/dashboard-app`
     * `/learn/dashboard-app/getting-started`
     * Any other course paths under `/learn/...`.

4. `is_internal_link(href: str) -> bool`

   * Treat as internal if:

     * Absolute: `href` starts with `https://nextjs.org/learn` or `https://www.nextjs.org/learn`
     * Root-relative: `href` starts with `/learn`
   * Everything else is external.

5. `derive_output_path(url: str) -> Path`

   * Base directory: `output_root / "nextjs-learn"` (where `output_root` is provided by the existing crawler config).
   * Mapping:

     * `/learn` → `nextjs-learn/index.md`
     * `/learn/<segment>` → `nextjs-learn/<segment>/index.md`
     * `/learn/<segment1>/<segment2>/.../<segmentN>` →
       `nextjs-learn/<segment1>/<segment2>/.../<segmentN>.md`
   * Slugging:

     * Use raw path segment text for filenames and directories (URL-decoded).
     * Replace characters invalid for filenames with `-`.
   * Examples:

     * `https://nextjs.org/learn` → `data/nextjs-learn/index.md`
     * `https://nextjs.org/learn/dashboard-app` → `data/nextjs-learn/dashboard-app/index.md` ([Next.js][2])
     * `https://nextjs.org/learn/dashboard-app/getting-started` → `data/nextjs-learn/dashboard-app/getting-started.md` ([Next.js][3])

6. `rewrite_link(href: str, from_url: str) -> str`

   * Input:

     * `href`: link as appears in HTML/markdown.
     * `from_url`: canonical URL of the page being processed.
   * Behavior:

     1. If `is_internal_link(href)` is false → return `href` unchanged.
     2. Convert `href` into a canonical absolute URL under `https://nextjs.org/learn...`.
     3. Compute `target_path = derive_output_path(target_url)`.
     4. Compute `source_path = derive_output_path(from_url)`.
     5. Compute a relative path from `source_path` directory to `target_path`.
   * Return that relative path as the rewritten link.
   * Example:

     * From page `https://nextjs.org/learn/dashboard-app/getting-started` (`data/nextjs-learn/dashboard-app/getting-started.md`) ([Next.js][3])

       * Link to `https://nextjs.org/learn/dashboard-app` → `../index.md`
       * Link to `/learn/dashboard-app/css-styling` → `./css-styling.md` (assuming that path exists and maps accordingly).

7. Optional: `postprocess_markdown(path: Path) -> None`

   * No Next.js-specific logic required beyond generic cleanup unless you see a need to strip navigation/footer boilerplate. If a generic postprocessing step already exists, reuse it.

---

3. Changes in the crawler core

Adapt the existing crawler to use `NextjsLearnProfile` through the generic profile abstraction:

1. Profile loading

   * Add a profile registry function:

     * `load_profile(name: str) -> SiteProfile`
   * Register `"nextjs-learn"` → `NextjsLearnProfile()`.

2. CLI integration

   * Extend the CLI to accept `--site nextjs-learn`.
   * When `--site` is specified:

     * Use `load_profile(site_name)`.
     * Use `profile.start_urls` as seeds.
     * Use `profile.max_depth` as default `depth_limit` unless overridden explicitly.

3. BFS and crawl loop

   * Before enqueuing or crawling any URL:

     * Normalize with `profile.normalize_url`.
     * Skip if not `profile.in_scope(url)`.
   * When discovering children from a page:

     * Normalize each child URL.
     * Enqueue only if `profile.should_enqueue(child)` and depth is within `depth_limit`.

4. Output path derivation

   * Replace any direct logic that computes output paths for this site with:

     * `profile.derive_output_path(url)`
   * All content writes for Next.js Learn must go into `profile.output_root / "nextjs-learn"` via this method.

5. Link rewriting

   * Wherever links inside markdown are rewritten:

     * Use `profile.is_internal_link(href)`
     * Use `profile.rewrite_link(href, from_url)`
   * Remove any Fullstack Open–specific URL patterns from this path.

---

4. Postprocess and linkcheck alignment

If separate scripts handle postprocessing and link checking:

1. Ensure they load the same profile

   * Accept `--site nextjs-learn` flag.
   * Call `load_profile("nextjs-learn")`.

2. Use the same link logic

   * Replace any in-script regexes that assume a different domain or path prefix with calls to:

     * `profile.in_scope`
     * `profile.is_internal_link`
     * `profile.rewrite_link`

3. Linkcheck rules

   * For Next.js Learn:

     * Treat all links that resolve to `nextjs-learn/...` under `profile.output_root` as internal and check they exist.
     * Treat others as external and skip or handle using existing external-link logic.

---

5. Crawl4AI and run config

Do not change the Crawl4AI integration beyond what is required to pass `NextjsLearnProfile` information:

* Seeds: `profile.start_urls`
* Respect `profile.max_depth` as the default `depth_limit`.
* Keep timeouts, concurrency, and selectors as-is unless they break on this site.

Ensure the HTML structure is compatible with current extraction logic:

* Course content appears as a central article-like document on chapter pages (headings, paragraphs, code blocks, etc.). ([Next.js][3])

If selectors need minor tweaks (e.g., to ignore top navigation/footer), implement them generically or behind profile-specific config, not hardcoded to this one site.

---

6. Acceptance criteria

7. Running the crawler with `--site nextjs-learn`:

   * Starts at `https://nextjs.org/learn`. ([Next.js][1])
   * Traverses through course overview and all reachable chapter pages under `/learn/...`.

8. Generated tree under `data/nextjs-learn`:

   * Contains:

     * `index.md` for `/learn`.
     * `dashboard-app/index.md` for `/learn/dashboard-app`. ([Next.js][2])
     * Additional files like `dashboard-app/getting-started.md` for chapter pages. ([Next.js][3])

9. Internal links inside markdown:

   * Links between Learn pages resolve to relative paths under `data/nextjs-learn/...`.
   * No remaining `https://nextjs.org/learn` or `/learn` absolute URLs inside markdown unless intentionally preserved as external references.

10. No Fullstack Open–specific assumptions are triggered when `--site nextjs-learn` is used; all behavior for this site is driven by `NextjsLearnProfile`.

[1]: https://nextjs.org/learn "Learn Next.js | Next.js by Vercel - The React Framework"
[2]: https://nextjs.org/learn/dashboard-app "App Router | Next.js"
[3]: https://nextjs.org/learn/dashboard-app/getting-started "App Router: Getting Started | Next.js"
