# parqtel.github.io

The public documentation site for [Parqtel](https://github.com/parqtel/parqtel-oss) — an ultra-lightweight, Rust-based SRE observability engine that streams OpenTelemetry metrics, logs, and traces into compressed Apache Parquet.

Served directly by GitHub Pages from the `main` branch.

## Documentation source

**The Markdown in `../rewritten-docs/` is the source of truth.** These HTML pages
are generated from it — do not hand-edit the `docs/` output.

```bash
cd ../rewritten-docs
python3 scripts/build_site.py            # Markdown -> HTML in this repo's docs/
python3 scripts/build_site.py --check    # report drift without writing
python3 scripts/check_docs.py            # link/anchor/heading validation
```

`build_site.py` renders Mermaid diagrams to inline SVG at build time, so the
published site has no client-side diagram dependency and works offline. It needs
the mermaid CLI (installed at `../.mermaid/`) and a Chrome binary. It also emits
`../sitemap.xml` and `../robots.txt`.

## Structure

```
.
├── index.html              # Landing page
├── 404.html                # Not-found page (noindex)
├── sitemap.xml             # GENERATED with the docs build
├── robots.txt              # GENERATED with the docs build
├── assets/
│   ├── css/site.css        # Design system
│   ├── js/site.js          # Theme toggle, mobile nav, copy buttons, scrollspy
│   └── img/                # Logo + screenshots
└── docs/                   # GENERATED — do not hand-edit
    ├── overview.html          # What Parqtel is, why, capabilities, limitations
    ├── getting-started.html   # Quickstart: install → first query
    ├── use-cases.html         # Fit, competitor comparison, when to choose else
    ├── architecture.html      # How it works: the request path end to end
    ├── storage.html           # Blocks, schemas, pruning, compaction, retention
    ├── durability.html        # Write-ahead log, commit protocol, recovery
    ├── performance.html       # Measured throughput, memory sizing, tuning
    ├── ingest.html            # Connect SDKs, collectors, sampling, pipelines
    ├── deployment.html        # Docker, Compose, Helm, Argo Rollouts, systemd
    ├── visualize.html         # Built-in console + Grafana
    ├── alerting.html          # Rules, state machine, notification routing
    ├── backup-upgrade.html    # Backup, restore, upgrade paths
    ├── troubleshooting.html   # Known limitations, sizing, profiling
    ├── configuration.html     # Every config key, env var
    ├── api.html               # Complete endpoint inventory
    ├── query-functions.html   # PromQL surface, PQL, divergences
    ├── cli.html               # Commands and flags
    ├── mcp.html               # MCP servers and their status
    ├── release-notes.html     # v0.3.1 / v0.3.0 / v0.2.0 / v0.1.0
    ├── faq.html               # FAQ + glossary
    ├── internals.html         # CONTRIBUTOR notes — not end-user documentation
    └── api-explorer.html      # GENERATED from the OpenAPI spec
```

## Information architecture

Pages are grouped into five sections, following the Diátaxis pattern:

| Section | Question it answers | Pages |
|---|---|---|
| **Introduction** | What is this and is it for me? | Overview · Quickstart · Use cases |
| **Concepts** | How does it work? | Architecture · Storage · Durability · Performance |
| **Guides** | How do I do X? | Ingest · Deploy · Visualise · Alerting · Backup · Troubleshoot |
| **Reference** | What exactly is this parameter? | Configuration · API · Query · CLI · MCP |
| **About** | What changed, and what does this term mean? | Release notes · FAQ |

## Documentation contract

These pages document **`parqtel-oss` as it is**, not as it is intended to be. Where
a feature is scaffolded but not wired, where a limit truncates silently, or where
a documented parameter is accepted but ignored, the docs say so plainly at the
point of use.

Implementation detail — crate layout, source paths, library versions — is
deliberately excluded from user-facing pages and preserved in
`docs/internals.html` for contributors.

Pages track release **v0.3.1**. The version in page footers and the badge is
generated from `VERSION` in `../rewritten-docs/scripts/build_site.py` — bump it
there, not in generated HTML.

## Design and accessibility

Every generated page carries a canonical URL, Open Graph and Twitter card
metadata, a JSON-LD `TechArticle` record, a skip link, and labelled navigation
landmarks. The landing page and 404 page follow the same conventions. The theme
respects `prefers-color-scheme`, persists a manual choice, and honours
`prefers-reduced-motion`. Focus rings are visible on all interactive elements.

## Editing

- Edit Markdown in `../rewritten-docs/`, then regenerate. Never edit `docs/*.html`
  by hand — the next build overwrites it.
- Add a page by writing the Markdown, then adding an entry to `PAGES` and
  `SIDEBAR_ORDER` in `../rewritten-docs/scripts/build_site.py`.
- Design changes go in `assets/css/site.css`.
- Every page carries the same nav, sidebar, and 4-column footer — these are
  generated from the registry in `build_site.py`, so they stay consistent
  automatically.

### `api-explorer.html` is generated

Do not edit it by hand. It is rebuilt from the OpenAPI spec in the sibling
repository:

```bash
python3 scripts/gen_explorer.py     # reads ../parqtel-oss/openapi.yaml
```

The spec is **not authoritative** — it diverges from the running server in known
places. `docs/api.html` lists those divergences, and `docs/internals.html`
records the caveat.

## Validating

```bash
# From ../rewritten-docs: Markdown source checks and build drift
python3 scripts/check_docs.py
python3 scripts/build_site.py --check

# From this repo: internal href/src + anchor check
python3 scripts/check_links.py
```

Run both before publishing. `check_docs.py` validates links, anchors, and heading
structure in the Markdown; `build_site.py --check` confirms the published HTML is
in sync; `check_links.py` catches broken links in the final site (including the
hand-written landing page and `api-explorer.html`). The GitHub Actions workflow
in `.github/workflows/link-check.yml` runs the link check on every push and pull
request.

## Local preview

Open `index.html` directly, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Publishing

Push to `main`. GitHub Pages builds from the branch root automatically. No `CNAME`
is set — the site is served at `https://parqtel.github.io/`.