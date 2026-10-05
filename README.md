# parqtel.github.io

The public documentation site for [Parqtel](https://github.com/parqtel/parqtel-oss) — an ultra-lightweight, Rust-based SRE observability engine that streams OpenTelemetry metrics, logs, and traces into compressed Apache Parquet.

This is a **static site** (no build step). It is served directly by GitHub Pages from the `main` branch.

## Structure

```
.
├── index.html              # Landing page
├── 404.html                # Not-found page
├── assets/
│   ├── css/site.css        # Design system
│   ├── js/site.js          # Theme toggle, mobile nav, copy buttons, scrollspy
│   └── img/                # Logo + SVG diagrams (architecture, dataflow, storage, mcp-flow)
└── docs/
    ├── getting-started.html   # Install, ingest, first query
    ├── architecture.html      # Crates, data flow, storage/query/pipeline paths, concurrency
    ├── storage.html           # Block model, schemas, pruning chain, index, compaction
    ├── durability.html        # Write-ahead log, commit protocol, replay, recovery
    ├── performance.html       # Measured numbers, with method
    ├── deployment.html        # Container, Compose, Helm, Argo Rollouts, systemd
    ├── configuration.html     # Every config key, env var, CLI flag
    ├── operations.html        # Known issues and limitations
    ├── release-notes.html     # v0.3.1 / v0.3.0 / v0.2.0 / v0.1.0
    ├── api.html               # Endpoint inventory
    ├── query-functions.html   # PromQL surface and its divergences
    ├── mcp.html               # MCP servers and their current status
    ├── faq.html               # FAQ + glossary
    ├── screenshots.html       # Console walkthrough
    └── api-explorer.html      # GENERATED — do not hand-edit
```

## Documentation contract

These pages document **`parqtel-oss` as it is**, not as it is intended to be. Where a feature is scaffolded but not wired, where a doc and the code disagree, or where a limit truncates silently, the site says so plainly and links to the source. Keep it that way when editing.

Pages are aligned to the **v0.3.1** release; the footer badge reads `Docs track v0.3.1`. When a release lands, update that string on every page.

## Editing

Pages are plain HTML that share a header, footer, sidebar, and the `assets/` design system. Diagrams are hand-drawn inline SVG (no external dependencies), so they render offline and on GitHub Pages alike.

- Edit CSS in `assets/css/site.css`.
- Edit diagrams in `assets/img/*.svg`.
- Add a doc page under `docs/` and link it from the nav, footer, **and** sidebar.
- Every `docs/` page carries the same 13-link sidebar and 4-column footer — copy them from an existing page rather than writing them fresh.

### `api-explorer.html` is generated

Do not edit it by hand. It is rebuilt from the OpenAPI spec in the sibling repository:

```bash
python3 scripts/gen_explorer.py     # reads ../parqtel-oss/openapi.yaml
```

The spec is not authoritative — see the *OpenAPI spec accuracy* section of `docs/api.html` for the known code-vs-spec divergences.

## Validating

```bash
python3 scripts/check_links.py      # internal href/src + anchor check; exits 1 on a break
```

Run this before publishing. It catches the most common breakage on a static site: an anchor that no longer exists because a heading was renamed.

## Local preview

Open `index.html` directly, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Publishing

Push to `main`. GitHub Pages builds from the branch root automatically. No `CNAME` is set — the site is served at `https://parqtel.github.io/`.
