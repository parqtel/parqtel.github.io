#!/usr/bin/env python3
"""Check internal links and anchors across the static site.

Dependency-free: parses local HTML, resolves relative href/src against the
file's directory, and verifies the target file (and optional #anchor) exists.
External (http/https), mailto:, tel:, and data: links are skipped.

Usage:  python3 scripts/check_links.py
Exit code 1 if any broken internal link is found.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ATTR_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]*)"', re.IGNORECASE)
ID_RE = re.compile(r'\bid\s*=\s*"([^"]+)"', re.IGNORECASE)
NAME_RE = re.compile(r'\bname\s*=\s*"([^"]+)"', re.IGNORECASE)

SKIP_PREFIXES = ("http://", "https://", "//", "mailto:", "tel:", "data:", "blob:")


def ids_in(path):
    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return set()
    return set(ID_RE.findall(text)) | set(NAME_RE.findall(text))


def main():
    errors = []
    html_files = []
    for dirpath, _, names in os.walk(ROOT):
        if ".git" in dirpath.split(os.sep):
            continue
        for n in names:
            if n.endswith(".html"):
                html_files.append(os.path.join(dirpath, n))
    html_files.sort()

    for f in html_files:
        rel = os.path.relpath(f, ROOT)
        text = open(f, encoding="utf-8", errors="ignore").read()
        base = os.path.dirname(f)
        for val in ATTR_RE.findall(text):
            if not val or val.startswith(SKIP_PREFIXES):
                continue
            if val.startswith("#"):
                frag = val[1:]
                if frag and frag not in ids_in(f):
                    errors.append(f"{rel}: anchor #{frag} not found on page")
                continue
            path, _, frag = val.partition("#")
            target = os.path.normpath(os.path.join(base, path)) if path else f
            if not os.path.exists(target):
                errors.append(f"{rel}: '{val}' -> missing file {os.path.relpath(target, ROOT)}")
            elif frag and frag not in ids_in(target):
                errors.append(f"{rel}: '{val}' -> #{frag} not found in {os.path.relpath(target, ROOT)}")

    if errors:
        print("Broken links found:\n  - " + "\n  - ".join(errors))
        sys.exit(1)
    print(f"OK: checked {len(html_files)} HTML files, no broken internal links.")


if __name__ == "__main__":
    main()
