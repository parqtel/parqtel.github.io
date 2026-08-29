#!/usr/bin/env python3
"""Generate docs/api-explorer.html from ../parqtel-oss/openapi.yaml.

Renders a dependency-free, filterable API explorer. Re-run after editing the
OpenAPI spec:  python3 scripts/gen_explorer.py
"""
import json
import os
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "..", "parqtel-oss", "openapi.yaml")
OUT = os.path.join(ROOT, "docs", "api-explorer.html")

METHOD_ORDER = ["get", "post", "put", "patch", "delete"]
ORDER = {"get": 0, "post": 1, "put": 2, "patch": 3, "delete": 4}


def load_spec():
    with open(SPEC, encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_operations(spec):
    ops = []
    for path, item in (spec.get("paths") or {}).items():
        for method in METHOD_ORDER:
            if method not in item:
                continue
            op = item[method]
            params = []
            for p in op.get("parameters", []) or []:
                sch = p.get("schema", {})
                params.append({
                    "name": p.get("name", ""),
                    "in": p.get("in", ""),
                    "required": bool(p.get("required", False)),
                    "type": sch.get("type", sch.get("schema", {}).get("type", "")) or (sch.get("items", {}).get("type", "") or ""),
                    "desc": (p.get("description") or "").strip(),
                })
            responses = []
            for code, r in (op.get("responses", {}) or {}).items():
                responses.append({"code": str(code), "desc": (r.get("description") or "").strip()})
            ops.append({
                "method": method,
                "path": path,
                "tag": (op.get("tags") or ["Other"])[0],
                "summary": (op.get("summary") or "").strip(),
                "description": (op.get("description") or "").strip(),
                "operationId": op.get("operationId", ""),
                "params": params,
                "hasBody": "requestBody" in op,
                "responses": responses,
            })
    return ops


def tag_order(spec):
    tags = [t.get("name") for t in spec.get("tags", []) if t.get("name")]
    seen = []
    for op in build_operations(spec):
        if op["tag"] not in seen:
            seen.append(op["tag"])
    for t in tags:
        if t not in seen:
            seen.append(t)
    return seen


NAV = '''      <a class="brand" href="../index.html"><img class="logo" src="../assets/img/logo.svg" alt="Parqtel"> Parqtel <small>Docs</small></a>
      <button class="icon-btn nav-toggle" aria-label="Toggle menu"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
      <nav class="nav-links" id="navLinks">
        <a href="architecture.html">Architecture</a>
        <a href="getting-started.html">Get Started</a>
        <a href="deployment.html">Deploy</a>
        <a href="mcp.html">MCP</a>
        <a href="api.html">API</a>
        <a href="screenshots.html">UI</a>
      </nav>
      <a class="icon-btn github-link" href="https://github.com/parqtel/parqtel-oss" aria-label="GitHub" style="margin-left:12px"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg></a>
      <button class="icon-btn" data-theme-toggle aria-label="Switch theme"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></svg></button>'''

SIDEBAR = '''      <div class="group-label">Reference</div>
      <a href="api.html">API Reference</a>
      <a href="api-explorer.html">API Explorer</a>
      <a href="query-functions.html">Query Functions</a>
      <a href="mcp.html">MCP Servers</a>
      <a href="faq.html">FAQ</a>
      <div class="group-label">UI</div>
      <a href="screenshots.html">Screenshots</a>
      <div class="group-label">Learn</div>
      <a href="architecture.html">Architecture</a>
      <a href="getting-started.html">Get Started</a>
      <a href="deployment.html">Deployment</a>
      <a href="configuration.html">Configuration</a>'''

FOOTER = '''      <div class="footer-grid">
        <div><a class="brand" href="../index.html"><img class="logo" src="../assets/img/logo.svg" alt="Parqtel"> Parqtel</a><p class="blurb" style="margin-top:10px">Ultra-lightweight SRE observability engine — streaming OTel signals into compressed Parquet.</p></div>
        <div><h5>Documentation</h5><a href="getting-started.html">Get Started</a><a href="architecture.html">Architecture</a><a href="deployment.html">Deployment</a><a href="configuration.html">Configuration</a><a href="api.html">API Reference</a><a href="api-explorer.html">API Explorer</a><a href="query-functions.html">Query Functions</a></div>
        <div><h5>Integrations</h5><a href="mcp.html">MCP Servers</a><a href="screenshots.html">UI Screenshots</a><a href="faq.html">FAQ</a><a href="https://github.com/parqtel/parqtel-oss/blob/main/docs/TROUBLESHOOTING.md">Troubleshooting</a><a href="https://github.com/parqtel/parqtel-oss/blob/main/docs/benchmarks/PERFORMANCE.md">Benchmarks</a></div>
        <div><h5>Project</h5><a href="https://github.com/parqtel/parqtel-oss">GitHub</a><a href="https://github.com/parqtel/parqtel-oss/blob/main/LICENSE">License</a><a href="https://github.com/parqtel/parqtel-oss/security">Security</a><a href="https://github.com/parqtel/parqtel-oss/blob/main/CONTRIBUTING.md">Contributing</a></div>
      </div>'''


def main():
    spec = load_spec()
    ops = build_operations(spec)
    tags = tag_order(spec)
    data = json.dumps({"tags": tags, "ops": ops}, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>API Explorer · Parqtel Docs</title>
  <meta name="description" content="Interactive OpenAPI 3.0 explorer for the Parqtel HTTP API — filter endpoints, inspect parameters, and see request/response shapes.">
  <link rel="icon" href="../assets/img/logo.svg">
  <link rel="stylesheet" href="../assets/css/site.css">
</head>
<body>
  <header class="nav"><div class="container nav-inner">
{NAV}
  </div></header>

  <div class="container docs-layout">
    <aside class="sidebar">
{SIDEBAR}
    </aside>

    <main class="docs-main">
      <h1>API Explorer</h1>
      <p class="lead">An interactive view of the Parqtel OpenAPI 3.0 contract. Search to filter, expand an operation to see its parameters and responses. The live spec is served at <code class="inline">/oas</code>.</p>
      <div class="codeblock"><button class="copy-btn">Copy</button><pre><code>curl http://localhost:9090/oas   # OpenAPI 3.0 specification</code></pre></div>

      <div style="margin:18px 0;display:flex;gap:10px;flex-wrap:wrap;align-items:center">
        <input id="apifilter" type="search" placeholder="Filter by path, method, or summary…" style="flex:1;min-width:240px;padding:10px 12px;border-radius:10px;border:1px solid var(--border-strong);background:var(--surface);color:var(--text);font-size:.95rem">
        <span id="apicount" class="tag">0 operations</span>
      </div>

      <div id="explorer"></div>
    </main>
  </div>

  <footer class="footer"><div class="container">
{FOOTER}
    <div class="footer-bottom"><span>© 2025 Parqtel. Apache-2.0 licensed.</span><span>Built with Rust · Axum · Apache Parquet</span></div>
  </div></footer>
  <script id="spec" type="application/json">{data}</script>
  <script src="../assets/js/site.js"></script>
  <script>
  (function () {{
    var spec = JSON.parse(document.getElementById('spec').textContent);
    var badges = {{get:'get',post:'post',put:'put',del:'del',patch:'patch'}};
    var explorer = document.getElementById('explorer');
    var filter = document.getElementById('apifilter');
    var count = document.getElementById('apicount');

    function esc(s) {{ return (s||'').replace(/[&<>"']/g, function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c];}}); }}

    function opCard(op) {{
      var b = badges[op.method] || 'get';
      var paramsHtml = op.params.length ? (
        '<table><thead><tr><th>Name</th><th>In</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody>' +
        op.params.map(function(p){{
          return '<tr><td><code class="inline">'+esc(p.name)+'</code></td><td>'+esc(p.in)+'</td><td>'+esc(p.type||'')+'</td><td>'+(p.required?'yes':'no')+'</td><td>'+esc(p.desc)+'</td></tr>';
        }}).join('') + '</tbody></table>'
      ) : '<p class="muted">No parameters.</p>';
      var bodyHtml = op.hasBody ? '<p><span class="badge-tag post">BODY</span> Accepts a request body (see the <a href="https://github.com/parqtel/parqtel-oss/blob/main/openapi.yaml">OpenAPI spec</a>).</p>' : '';
      var respHtml = op.responses.length ? (
        '<table><thead><tr><th>Code</th><th>Description</th></tr></thead><tbody>' +
        op.responses.map(function(r){{ return '<tr><td><code class="inline">'+esc(r.code)+'</code></td><td>'+esc(r.desc)+'</td></tr>'; }}).join('') + '</tbody></table>'
      ) : '';
      var desc = op.description && op.description !== op.summary ? '<p>'+esc(op.description)+'</p>' : '';
      return '<div class="op" data-text="'+(op.method+' '+op.path+' '+op.summary+' '+op.tag).toLowerCase()+'" style="border:1px solid var(--border);border-radius:12px;margin:10px 0;overflow:hidden">' +
        '<button class="op-head" style="width:100%;display:flex;gap:12px;align-items:center;text-align:left;padding:12px 14px;background:var(--surface);border:0;cursor:pointer;color:var(--text)">' +
          '<span class="badge-tag '+b+'">'+op.method.toUpperCase()+'</span>' +
          '<code class="inline" style="font-size:.92rem">'+esc(op.path)+'</code>' +
          '<span style="color:var(--text-muted);margin-left:auto;font-size:.9rem">'+esc(op.summary)+'</span>' +
        '</button>' +
        '<div class="op-body" style="display:none;padding:4px 14px 16px;border-top:1px solid var(--border)">'+desc+bodyHtml+paramsHtml+respHtml+'</div>' +
      '</div>';
    }}

    function render() {{
      var html = '';
      spec.tags.forEach(function(tag) {{
        var list = spec.ops.filter(function(o){{return o.tag===tag;}});
        if (!list.length) return;
        html += '<h2 id="tag-'+esc(tag)+'">'+esc(tag)+'</h2><div class="tag-group">';
        html += list.map(opCard).join('');
        html += '</div>';
      }});
      explorer.innerHTML = html;
      Array.prototype.forEach.call(explorer.querySelectorAll('.op-head'), function(h){{
        h.addEventListener('click', function(){{ var b=h.nextElementSibling; b.style.display = b.style.display==='none'?'block':'none'; }});
      }});
    }}

    function applyFilter() {{
      var q = filter.value.trim().toLowerCase();
      var shown = 0;
      Array.prototype.forEach.call(explorer.querySelectorAll('.op'), function(card){{
        var match = !q || card.getAttribute('data-text').indexOf(q) !== -1;
        card.style.display = match ? '' : 'none';
        if (match) shown++;
      }});
      // hide empty tag headers
      Array.prototype.forEach.call(explorer.querySelectorAll('h2'), function(h){{
        var grp = h.nextElementSibling;
        if (grp && grp.classList.contains('tag-group')) {{
          var any = Array.prototype.some.call(grp.querySelectorAll('.op'), function(c){{return c.style.display!=='none';}});
          h.style.display = any ? '' : 'none';
        }}
      }});
      count.textContent = shown + ' operation' + (shown===1?'':'s');
    }}

    render();
    applyFilter();
    filter.addEventListener('input', applyFilter);
  }})();
  </script>
</body>
</html>"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {OUT}: {len(ops)} operations, {len(tags)} tags")


if __name__ == "__main__":
    main()
