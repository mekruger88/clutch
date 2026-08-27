#!/usr/bin/env python3
"""Documentation checks. No third-party dependencies.

1. Every relative Markdown link resolves to a file that exists.
2. Every docs/adr/NNNN-*.md is listed in the ADR index.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
failures = []

for md in ROOT.rglob("*.md"):
    if ".github" in md.parts:
        continue
    text = md.read_text(encoding="utf-8")
    for target in LINK.findall(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#")[0].strip()
        if not clean:
            continue
        resolved = (md.parent / clean).resolve()
        if not resolved.exists():
            rel = md.relative_to(ROOT)
            failures.append(f"broken link in {rel}: {target}")

adr_dir = ROOT / "docs" / "adr"
index = adr_dir / "README.md"
if index.exists():
    index_text = index.read_text(encoding="utf-8")
    for adr in sorted(adr_dir.glob("[0-9][0-9][0-9][0-9]-*.md")):
        number = adr.name[:4]
        if number not in index_text:
            failures.append(f"ADR {adr.name} is not listed in docs/adr/README.md")
else:
    failures.append("docs/adr/README.md is missing")

if failures:
    print("FAIL")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print("OK: doc links resolve and every ADR is indexed")
