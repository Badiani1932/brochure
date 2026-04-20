#!/usr/bin/env python3
"""
Site-wide optimization of heavy assets actually referenced in production.

Target (critical, referenced & preloaded / used in modals / catalog):
  - assets/images/migrated/eventi/CT FIRENZE/food-list-modal.webp  (4.5 MB)
  - assets/images/migrated/eventi/CT FIRENZE/drink-list-modal.webp (3.0 MB)
  - assets/gelato/Bacio/bacio.png                                   (7.1 MB)
  - assets/gelato/Bacio/bacio-dettaglio.jpeg                        (3.0 MB)
  - All assets/gelato/**/*.webp > 1 MB  (catalogo gelati)
  - assets/images/migrated/eventi/foto eventi/3.webp                (1.8 MB)

For JPG/PNG sources we output WebP alongside and keep the original as-is
(referenced by catalog; we update the .js/.html where needed).
For WebP sources we overwrite in place after resizing/re-encoding.

Originals are backed up into an `_originals/` subfolder per location.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent

# (relative_path, max_edge_px, webp_quality)
CRITICAL_FILES: list[tuple[str, int, int]] = [
    ("assets/images/migrated/eventi/CT FIRENZE/food-list-modal.webp", 1800, 75),
    ("assets/images/migrated/eventi/CT FIRENZE/drink-list-modal.webp", 1800, 75),
    ("assets/gelato/Bacio/bacio.png", 1600, 75),
    ("assets/gelato/Bacio/bacio-dettaglio.jpeg", 1600, 75),
    ("assets/images/migrated/eventi/foto eventi/3.webp", 1600, 72),
    ("assets/images/migrated/eventi/foto eventi/5.webp", 1600, 72),
    ("assets/images/migrated/eventi/foto eventi/2.webp", 1600, 72),
]

# Auto: all gelato webp > 1 MB
GELATO_DIR = ROOT / "assets" / "gelato"
GELATO_THRESHOLD = 1_000_000
GELATO_MAX_EDGE = 1400
GELATO_QUALITY = 72


def backup(src: Path) -> Path:
    bdir = src.parent / "_originals"
    bdir.mkdir(exist_ok=True)
    bpath = bdir / src.name
    if not bpath.exists():
        shutil.copy2(src, bpath)
    return bpath


def optimize_webp_inplace(src: Path, max_edge: int, quality: int) -> tuple[int, int]:
    bpath = backup(src)
    before = bpath.stat().st_size
    with Image.open(bpath) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
        img.thumbnail((max_edge, max_edge), Image.LANCZOS)
        img.save(src, format="WEBP", quality=quality, method=6)
    return before, src.stat().st_size


def optimize_to_webp(src: Path, max_edge: int, quality: int) -> tuple[Path, int, int]:
    """Non-webp source (png/jpg): write sibling .webp, keep original untouched."""
    dst = src.with_suffix(".webp")
    with Image.open(src) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
        img.thumbnail((max_edge, max_edge), Image.LANCZOS)
        if img.mode == "RGBA":
            img.save(dst, format="WEBP", quality=quality, method=6)
        else:
            img.save(dst, format="WEBP", quality=quality, method=6)
    return dst, src.stat().st_size, dst.stat().st_size


def main() -> None:
    total_before = 0
    total_after = 0
    lines: list[str] = []

    # Critical named files
    for rel, max_edge, q in CRITICAL_FILES:
        src = ROOT / rel
        if not src.exists():
            print(f"  skip (missing): {rel}")
            continue
        if src.suffix.lower() == ".webp":
            before, after = optimize_webp_inplace(src, max_edge, q)
            lines.append(f"  {rel}: {before/1024:.0f} KB -> {after/1024:.0f} KB")
            total_before += before
            total_after += after
        else:
            dst, before, after = optimize_to_webp(src, max_edge, q)
            lines.append(
                f"  {rel} -> {dst.name}: {before/1024:.0f} KB -> {after/1024:.0f} KB"
            )
            total_before += before
            total_after += after

    # Auto gelato webp > 1 MB
    if GELATO_DIR.exists():
        for src in sorted(GELATO_DIR.rglob("*.webp")):
            if "_originals" in src.parts:
                continue
            if src.stat().st_size <= GELATO_THRESHOLD:
                continue
            before, after = optimize_webp_inplace(src, GELATO_MAX_EDGE, GELATO_QUALITY)
            rel = src.relative_to(ROOT).as_posix()
            lines.append(f"  {rel}: {before/1024:.0f} KB -> {after/1024:.0f} KB")
            total_before += before
            total_after += after

    for l in lines:
        print(l)

    print("\n---")
    print(f"Before: {total_before/1024/1024:.2f} MB")
    print(f"After:  {total_after/1024/1024:.2f} MB")
    if total_before:
        saved = total_before - total_after
        print(f"Saved:  {saved/1024/1024:.2f} MB ({saved/total_before*100:.1f}%)")


if __name__ == "__main__":
    main()
