"""Remove orphaned Coni/Coppette CSS from b2b/index.html.
   Removes:
   - Main CSS block: .coni-*, .coppette-*, .conigf-* (~800 lines)
   - Media query entries referencing .coppette-map-wrapper, .coni-map-wrapper, .conigf-map-wrapper
"""
import pathlib, re

fp = pathlib.Path(r'b2b/index.html')
src = fp.read_text(encoding='utf-8')
orig_len = len(src)

# ──────────────────────────────────────────────────────────────
# 1. Remove main CSS block: from "/* -- Coni & Coppette gallery -- */"
#    up to but not including "/* -- Accessori interactive hero map -- */"
# ──────────────────────────────────────────────────────────────
marker_start = "    /* -- Coni & Coppette gallery -- */"
marker_end = "    /* -- Accessori interactive hero map -- */"
i1 = src.index(marker_start)
i2 = src.index(marker_end, i1)
removed_css = src[i1:i2]
src = src[:i1] + src[i2:]
print(f"1. Removed main CSS block ({len(removed_css)} chars, {removed_css.count(chr(10))} lines)")

# ──────────────────────────────────────────────────────────────
# 2. Remove media query entries from @media blocks that reference
#    orphaned selectors (.coppette-map-wrapper, .coni-map-wrapper, etc.)
# ──────────────────────────────────────────────────────────────
# These are typically in wide media queries that group multiple selectors.
# We need to match patterns like:
#   .coppette-map-wrapper,\n      .coni-map-wrapper,\n      .conigf-map-wrapper,\n

orphaned_classes = [
    'coppette-map-wrapper', 'coni-map-wrapper', 'conigf-map-wrapper',
    'coni-grid', 'coni-card', 'coni-meta', 'coni-gf-btn', 'coni-gf-details',
    'coppette-zone', 'coni-zone', 'conigf-zone',
    'coppette-detail', 'coni-detail', 'conigf-detail',
    'coppette-hero-section', 'coni-hero-section', 'conigf-hero-section',
    'coppette-hint', 'coni-hint', 'conigf-hint',
]

# Remove individual lines that contain ONLY an orphaned class as a selector
# Pattern: whitespace + .orphaned-class-name + optional-comma + newline
for cls in orphaned_classes:
    pattern = re.compile(r'^\s+\.' + re.escape(cls) + r'[^{]*?[,]\s*\n', re.MULTILINE)
    count = len(pattern.findall(src))
    if count:
        src = pattern.sub('', src)
        print(f"   Removed {count} lines containing .{cls} (selectors)")

# Also remove entire rules that start with an orphaned class
for cls in orphaned_classes:
    pattern = re.compile(r'^\s+\.' + re.escape(cls) + r'\{[^}]*\}\s*\n', re.MULTILINE)
    count = len(pattern.findall(src))
    if count:
        src = pattern.sub('', src)
        print(f"   Removed {count} standalone rules for .{cls}")

# ──────────────────────────────────────────────────────────────
# Verify no orphaned references remain
# ──────────────────────────────────────────────────────────────
remaining = []
for cls in ['coni-grid', 'coni-card', 'coppette-map', 'coni-map-wrapper',
            'conigf-map', 'coppette-zone', 'coni-zone-label', 'conigf-zone-label',
            'coppette-detail-panel', 'coni-detail-panel', 'conigf-detail-panel',
            'coppette-hero-section', 'coni-hero-section', 'conigf-hero-section',
            'coni-hint', 'coppette-hint', 'conigf-hint']:
    cnt = src.count(cls)
    if cnt > 0:
        remaining.append(f"  .{cls}: {cnt} occurrences")

if remaining:
    print("\nWARNING: Some orphaned class references still found:")
    for r in remaining:
        print(r)
else:
    print("\n✓ No orphaned CSS class references remain")

fp.write_text(src, encoding='utf-8')
new_len = len(src)
print(f"\nDone. {orig_len} -> {new_len} chars ({orig_len - new_len} chars removed)")
