#!/usr/bin/env python3
"""
Optimize carretto_gelato modal images.

Source: assets/images/eventi/carretto_gelato/fotoN.jpg (2.8–5.7 MB each)
Output (same folder):
  - fotoN.webp  (main, WebP q72, max edge 1600)
  - fotoN.jpg   (overwritten: re-encoded JPEG q80, max edge 1600, progressive)

Originals are backed up to assets/images/eventi/carretto_gelato/_originals/
"""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / "assets" / "images" / "eventi" / "carretto_gelato"
BACKUP = FOLDER / "_originals"

MAX_EDGE = 1600
WEBP_QUALITY = 72
JPEG_QUALITY = 80


def process(src: Path) -> tuple[int, int, int]:
    BACKUP.mkdir(exist_ok=True)
    backup_path = BACKUP / src.name
    if not backup_path.exists():
        shutil.copy2(src, backup_path)

    before = backup_path.stat().st_size

    with Image.open(backup_path) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)

        webp_path = src.with_suffix(".webp")
        img.save(webp_path, format="WEBP", quality=WEBP_QUALITY, method=6)

        img.save(
            src,
            format="JPEG",
            quality=JPEG_QUALITY,
            optimize=True,
            progressive=True,
        )

    return before, src.stat().st_size, webp_path.stat().st_size


def main() -> None:
    total_before = total_jpg = total_webp = 0
    count = 0
    for src in sorted(FOLDER.glob("foto*.jpg")):
        before, jpg_after, webp_after = process(src)
        total_before += before
        total_jpg += jpg_after
        total_webp += webp_after
        count += 1
        print(
            f"✓ {src.name}: {before/1024:.0f} KB "
            f"-> jpg {jpg_after/1024:.0f} KB, webp {webp_after/1024:.0f} KB"
        )

    if not count:
        print("No files found.")
        return

    print("\n---")
    print(f"Files: {count}")
    print(f"Before:     {total_before/1024/1024:.2f} MB")
    print(f"After JPEG: {total_jpg/1024/1024:.2f} MB")
    print(f"After WebP: {total_webp/1024/1024:.2f} MB")
    saved = total_before - total_webp
    print(f"Saved vs WebP: {saved/1024/1024:.2f} MB ({saved/total_before*100:.1f}%)")


if __name__ == "__main__":
    main()
