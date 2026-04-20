#!/usr/bin/env python3
"""
Compress heavy hero videos (keep visual quality, add web-streaming flags).

Targets (referenced in production):
  - assets/video/videotosinghi.mp4        (8.4 MB)   loop hero saletta-privata-tosinghi
  - assets/video/b2b homepage video.mp4   (13.8 MB)  hero b2b home

Technique:
  - H.264 CRF 24, preset slow, max 1080p (downscale if larger)
  - AAC audio if present (most hero loops are muted: we strip audio)
  - +faststart (moov atom at front -> plays while downloading)

Originals backed up to assets/video/_originals/
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEO_DIR = ROOT / "assets" / "video"
BACKUP = VIDEO_DIR / "_originals"

TARGETS = [
    "videotosinghi.mp4",
    "b2b homepage video.mp4",
]

MAX_HEIGHT = 1080
CRF = 24
PRESET = "slow"


def compress(src: Path) -> tuple[int, int]:
    BACKUP.mkdir(exist_ok=True)
    bpath = BACKUP / src.name
    if not bpath.exists():
        shutil.copy2(src, bpath)

    before = bpath.stat().st_size
    tmp_out = src.with_suffix(".tmp.mp4")

    cmd = [
        "ffmpeg", "-y", "-i", str(bpath),
        "-vf", f"scale='min(1920,iw)':'min({MAX_HEIGHT},ih)':force_original_aspect_ratio=decrease",
        "-c:v", "libx264",
        "-preset", PRESET,
        "-crf", str(CRF),
        "-pix_fmt", "yuv420p",
        "-profile:v", "high",
        "-level", "4.0",
        "-an",  # strip audio (these are muted hero loops)
        "-movflags", "+faststart",
        str(tmp_out),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    tmp_out.replace(src)
    return before, src.stat().st_size


def main() -> None:
    total_before = total_after = 0
    for name in TARGETS:
        src = VIDEO_DIR / name
        if not src.exists():
            print(f"  skip (missing): {name}")
            continue
        print(f"  compressing {name} ...")
        before, after = compress(src)
        total_before += before
        total_after += after
        print(f"    {before/1024/1024:.2f} MB -> {after/1024/1024:.2f} MB")

    if total_before:
        saved = total_before - total_after
        print(f"\nTotal: {total_before/1024/1024:.2f} MB -> {total_after/1024/1024:.2f} MB "
              f"({saved/total_before*100:.1f}% smaller)")


if __name__ == "__main__":
    main()
