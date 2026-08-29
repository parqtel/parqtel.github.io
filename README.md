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
    ├── getting-started.html
    ├── architecture.html
    ├── deployment.html
    ├── configuration.html
    ├── api.html
    ├── query-functions.html
    ├── mcp.html
    └── faq.html
```

## Editing

Pages are plain HTML that share a header, footer, and the `assets/` design system. Diagrams are hand-drawn inline SVG (no external dependencies), so they render offline and on GitHub Pages alike.

- Edit CSS in `assets/css/site.css`.
- Edit diagrams in `assets/img/*.svg`.
- Add a doc page under `docs/` and link it from the nav/footer/sidebar.

## Local preview

Open `index.html` directly, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Publishing

Push to `main`. GitHub Pages builds from the branch root automatically. No `CNAME` is set — the site is served at `https://parqtel.github.io/`.
