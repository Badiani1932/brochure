#!/usr/bin/env python3
"""
Normalize asset file/folder names to ASCII kebab-case and auto-update references.

Scope:
  - Folders & files under assets/gelato/** with spaces, uppercase, underscores,
    accents or special chars.
  - assets/video/*.mp4 with spaces.

For each rename we update every occurrence of the OLD relative path in
{html,js,css} files (both raw and %-encoded variants).

Backups of touched text files are NOT kept (changes shown via git diff).
"""

from __future__ import annotations

import re
import shutil
import unicodedata
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
TEXT_EXT = {".html", ".js", ".css"}


def slugify(name: str, keep_ext: bool = True) -> str:
    stem, dot, ext = name.rpartition(".") if keep_ext and "." in name else (name, "", "")
    base = stem if stem else name
    # strip accents
    base = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode("ascii")
    base = base.lower()
    # replace any non-alphanum with dash
    base = re.sub(r"[^a-z0-9]+", "-", base)
    base = base.strip("-")
    if ext:
        ext = ext.lower()
        return f"{base}.{ext}"
    return base


def needs_rename(name: str) -> bool:
    """True if the file/dir name is not already a safe slug."""
    ext_split = name.rsplit(".", 1)
    if len(ext_split) == 2 and ext_split[1].isalnum():
        stem, ext = ext_split
    else:
        stem, ext = name, ""
    if stem != slugify(stem, keep_ext=False):
        return True
    if ext and ext != ext.lower():
        return True
    return False


def collect_renames() -> list[tuple[Path, Path]]:
    renames: list[tuple[Path, Path]] = []

    # Targets (restrict to these roots to keep blast radius predictable)
    roots = [
        ASSETS / "gelato",
        ASSETS / "video",
    ]

    for root in roots:
        if not root.exists():
            continue
        # Deepest first so child paths rename before parents
        all_items = sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True)
        for p in all_items:
            if "_originals" in p.parts:
                continue
            if not needs_rename(p.name):
                continue
            new_name = slugify(p.name, keep_ext=p.is_file())
            if not new_name or new_name == p.name:
                continue
            target = p.with_name(new_name)
            # Avoid collisions
            if target.exists() and target != p:
                print(f"  [skip collision] {p} -> {target}")
                continue
            renames.append((p, target))
    return renames


def build_replacement_map(renames: list[tuple[Path, Path]]) -> list[tuple[str, str]]:
    """Return list of (old_substring, new_substring) pairs to apply in text files.

    We emit both raw and URL-encoded variants (spaces -> %20, etc.).
    """
    pairs: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for old, new in renames:
        old_rel = old.relative_to(ROOT).as_posix()
        new_rel = new.relative_to(ROOT).as_posix()
        variants = {
            old_rel: new_rel,
            quote(old_rel, safe="/"): quote(new_rel, safe="/"),
            quote(old_rel, safe="/:"): quote(new_rel, safe="/:"),
        }
        for o, n in variants.items():
            if o == n:
                continue
            if (o, n) in seen:
                continue
            seen.add((o, n))
            pairs.append((o, n))
    # Apply longer strings first to avoid partial overlap issues
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


def update_text_files(pairs: list[tuple[str, str]]) -> int:
    if not pairs:
        return 0
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXT:
            continue
        # Skip things in backups / venv / node_modules
        parts = set(path.parts)
        if any(x in parts for x in {"_originals", ".venv", "node_modules", ".git"}):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new_text = text
        for old, new in pairs:
            if old in new_text:
                new_text = new_text.replace(old, new)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            rel = path.relative_to(ROOT).as_posix()
            print(f"  updated refs: {rel}")
            changed += 1
    return changed


def perform_renames(renames: list[tuple[Path, Path]]) -> None:
    # Do file renames first, then dir renames (children before parents already sorted)
    # But since sorted deepest-first, some parents come after - ensure dirs do not rename
    # until children are moved. We already did deepest-first so this works.
    for old, new in renames:
        if not old.exists():
            continue
        print(f"  rename: {old.relative_to(ROOT).as_posix()} -> {new.name}")
        # case-only rename on Windows needs two-step
        if old.name.lower() == new.name.lower() and old.name != new.name:
            tmp = old.with_name(old.name + ".__tmp__")
            old.rename(tmp)
            tmp.rename(new)
        else:
            old.rename(new)


def main() -> None:
    renames = collect_renames()
    if not renames:
        print("Nothing to rename.")
        return

    print(f"Planned renames: {len(renames)}")
    pairs = build_replacement_map(renames)
    print(f"Reference replacements to apply: {len(pairs)}")

    print("\n-- Updating text references --")
    touched = update_text_files(pairs)
    print(f"Text files updated: {touched}")

    print("\n-- Performing filesystem renames --")
    perform_renames(renames)
    print("Done.")


if __name__ == "__main__":
    main()
