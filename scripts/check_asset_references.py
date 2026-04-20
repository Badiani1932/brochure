#!/usr/bin/env python3
"""Check that every assets/... reference in HTML/JS/CSS resolves to an existing file."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
TEXT_EXT = {".html", ".js", ".css"}
SKIP_DIRS = {"_originals", ".venv", "node_modules", ".git"}

# Match relative paths to assets/
PATTERN = re.compile(r'["\'(]([^"\'()<>\s]*?assets/[^"\'()<>\s]+?)["\'()]')


def iter_text_files():
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in TEXT_EXT:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def resolve(ref: str, base: Path) -> Path | None:
    ref = unquote(ref)
    # strip leading ./ or ../
    candidate = (base.parent / ref).resolve()
    if candidate.exists():
        return candidate
    return None


def main() -> None:
    missing: list[tuple[str, str, int]] = []
    total = 0
    for f in iter_text_files():
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for m in PATTERN.finditer(text):
            ref = m.group(1)
            # Skip non-path literals
            if "\n" in ref:
                continue
            total += 1
            # Line number
            line_no = text.count("\n", 0, m.start()) + 1
            if resolve(ref, f) is None:
                rel = f.relative_to(ROOT).as_posix()
                missing.append((rel, ref, line_no))

    if not missing:
        print(f"OK - all {total} asset references resolve.")
        return

    print(f"MISSING {len(missing)} references out of {total}:\n")
    for file, ref, line in missing[:80]:
        print(f"  {file}:{line}  -> {ref}")
    if len(missing) > 80:
        print(f"  ... and {len(missing)-80} more")


if __name__ == "__main__":
    main()
