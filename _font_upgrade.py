"""
Bulk font-size upgrade script.
- General elements: aggressive increase (+4-5px, floor 15px)
- B2B gelato card elements: moderate increase (+2-3px, floor 13px)
- Titles (>=20px) and dvh clamps: untouched
"""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))

# Fixed font-size mappings (old → new)
GENERAL = {9:15, 10:15, 11:15, 12:16, 13:17, 14:18, 15:18}
B2B_CARD = {9:13, 10:13, 11:14, 12:15, 13:16, 14:16, 15:16}

# Keywords that identify B2B gelato-card context
CARD_KW = [
    'gelato-card','gelato-list','gelato-flag','gelato-control',
    'gelato-empty','gelato-section','tipologia','modal__table',
    'modal__note','modal__section','modal__nav','gelato-header',
    '.notice{','card__exp','gelato-badge',
]

def find_selector(lines, idx):
    for i in range(idx, max(idx-25, -1), -1):
        if '{' in lines[i]:
            return lines[i]
    return ""

def is_card_ctx(lines, idx):
    line = lines[idx]
    sel = find_selector(lines, idx)
    combined = line + sel
    return any(kw in combined for kw in CARD_KW)

def process(filepath, is_b2b=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    orig = list(lines)

    for i in range(len(lines)):
        ln = lines[i]
        if 'font-size' not in ln:
            continue

        if is_b2b and is_card_ctx(orig, i):
            fmap, d_min, d_vw, d_max, floor = B2B_CARD, 2, 0.2, 2, 13
        else:
            fmap, d_min, d_vw, d_max, floor = GENERAL, 4, 0.4, 4, 15

        # 1) clamp with vw
        def rvw(m):
            mn,vw,mx = int(m.group(1)),float(m.group(2)),int(m.group(3))
            if mn > 15: return m.group(0)
            nm = max(mn+d_min, floor)
            nv = round(vw+d_vw, 2)
            nx = mx+d_max
            if nx<=nm: nx=nm+3
            return f"clamp({nm}px, {nv}vw, {nx}px)"
        ln = re.sub(r'clamp\(\s*(\d+)px\s*,\s*([\d.]+)vw\s*,\s*(\d+)px\s*\)', rvw, ln)

        # 2) clamp with cqi (always moderate)
        def rcqi(m):
            mn,cq,mx = int(m.group(1)),float(m.group(2)),int(m.group(3))
            if mn > 15: return m.group(0)
            nm = mn+2; nq = round(cq+0.3,1); nx = mx+2
            if nx<=nm: nx=nm+3
            return f"clamp({nm}px, {nq}cqi, {nx}px)"
        ln = re.sub(r'clamp\(\s*(\d+)px\s*,\s*([\d.]+)cqi\s*,\s*(\d+)px\s*\)', rcqi, ln)

        # 3) dvh clamps: skip

        # 4) fixed font-size: Xpx (9-15px only)
        def rfix(m):
            pre,val,suf = m.group(1),int(m.group(2)),m.group(3)
            if val in fmap: return f"{pre}{fmap[val]}{suf}"
            return m.group(0)
        ln = re.sub(
            r'(font-size\s*:\s*)(\d+)(px)',
            lambda m: rfix(m) if 9<=int(m.group(2))<=15 else m.group(0), ln
        )

        lines[i] = ln

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    changed = sum(1 for a,b in zip(orig,lines) if a!=b)
    return changed

FILES = [
    ("assets/badiani-common.css", False),
    ("index.html", False),
    ("b2b/index.html", True),
    ("eventi/index.html", False),
    ("eventi/evento-esterno/index.html", False),
    ("eventi/experience/index.html", False),
    ("eventi/saletta-privata-tosinghi/index.html", False),
    ("eventi/speciale-aziende/index.html", False),
    ("magazine/index.html", False),
    ("cookie-policy.html", False),
    ("privacy.html", False),
]

total = 0
for rel, b2b in FILES:
    fp = os.path.join(BASE, rel)
    if os.path.exists(fp):
        n = process(fp, b2b)
        print(f"  {rel}: {n} lines changed")
        total += n
    else:
        print(f"  {rel}: NOT FOUND")
print(f"\n  TOTAL: {total} lines changed across {len(FILES)} files")
