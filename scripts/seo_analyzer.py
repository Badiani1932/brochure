#!/usr/bin/env python3
"""
SEO Analyzer — Badiani 1932 Brochure Site
Analizza tutti i file HTML per problemi SEO critici e fornisce un report dettagliato.
"""

import os
import sys
import re
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin

BASE_URL = "https://www.badiani1932.com"
ROOT = Path(__file__).parent.parent

# ── Colori ANSI ──────────────────────────────────────────────────────────────
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def color(text, c): return f"{c}{text}{RESET}"

# ── Parser HTML ───────────────────────────────────────────────────────────────
class SEOParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self._in_title = False
        self.metas = {}          # name/property → content
        self.links = []          # list of {rel, href, hreflang, type, ...}
        self.headings = []       # list of (level, text)
        self._cur_heading = None
        self._heading_text = []
        self.images = []         # list of {src, alt, loading}
        self.schema_ld = []      # list of raw JSON strings
        self._in_script_ld = False
        self._script_buf = []
        self.has_viewport = False
        self.has_charset = False
        self.canonical = None
        self.lang = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang", "")
        elif tag == "title":
            self._in_title = True
            self._title_buf = []
        elif tag == "meta":
            name = attrs.get("name", attrs.get("property", ""))
            content = attrs.get("content", "")
            if name:
                self.metas[name] = content
            if attrs.get("name") == "viewport":
                self.has_viewport = True
            if attrs.get("charset"):
                self.has_charset = True
            if attrs.get("http-equiv", "").lower() == "content-type":
                self.has_charset = True
        elif tag == "link":
            self.links.append(attrs)
            if attrs.get("rel") == "canonical":
                self.canonical = attrs.get("href", "")
        elif tag in ("h1","h2","h3","h4","h5","h6"):
            self._cur_heading = tag
            self._heading_text = []
        elif tag == "img":
            self.images.append({
                "src": attrs.get("src", ""),
                "alt": attrs.get("alt"),          # None = missing attr
                "loading": attrs.get("loading", ""),
                "aria-hidden": attrs.get("aria-hidden", "")
            })
        elif tag == "script":
            if attrs.get("type") == "application/ld+json":
                self._in_script_ld = True
                self._script_buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
            self.title = "".join(self._title_buf).strip()
        elif tag in ("h1","h2","h3","h4","h5","h6") and self._cur_heading == tag:
            self.headings.append((tag, "".join(self._heading_text).strip()))
            self._cur_heading = None
        elif tag == "script" and self._in_script_ld:
            self.schema_ld.append("".join(self._script_buf))
            self._in_script_ld = False

    def handle_data(self, data):
        if self._in_title:
            self._title_buf.append(data)
        elif self._cur_heading:
            self._heading_text.append(data)
        elif self._in_script_ld:
            self._script_buf.append(data)

# ── Analisi singola pagina ────────────────────────────────────────────────────
def analyze_file(path: Path):
    issues   = []  # [("critical"|"warning"|"ok", message)]
    
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return [("critical", f"Impossibile leggere il file: {e}")], {}, path

    # Encoding corruption check
    if "â€" in text:
        occ = text.count("â€")
        issues.append(("critical", f"Encoding corrotto: trovate {occ} occorrenze di 'â€' (dovrebbe essere '—' o caratteri accentati)"))
    if "Ã©" in text or "Ã¨" in text or "Ã" in text:
        issues.append(("critical", "Encoding corrotto: trovate sequenze Ã© Ã¨ (caratteri accentati mal codificati)"))

    p = SEOParser()
    try:
        p.feed(text)
    except Exception:
        pass

    # ── HTML lang ────────────────────────────────────────────────────────────
    if not p.lang:
        issues.append(("critical", "Attributo lang mancante su <html>"))
    else:
        issues.append(("ok", f"lang=\"{p.lang}\""))

    # ── Charset ──────────────────────────────────────────────────────────────
    if not p.has_charset:
        issues.append(("critical", "Meta charset mancante"))
    else:
        issues.append(("ok", "Meta charset presente"))

    # ── Viewport ─────────────────────────────────────────────────────────────
    if not p.has_viewport:
        issues.append(("critical", "Meta viewport mancante"))
    else:
        issues.append(("ok", "Meta viewport presente"))

    # ── Title ─────────────────────────────────────────────────────────────────
    if not p.title:
        issues.append(("critical", "Title tag mancante"))
    elif len(p.title) < 30:
        issues.append(("warning", f"Title troppo corto ({len(p.title)} chars): \"{p.title}\""))
    elif len(p.title) > 65:
        issues.append(("warning", f"Title troppo lungo ({len(p.title)} chars): \"{p.title[:60]}…\""))
    else:
        issues.append(("ok", f"Title OK ({len(p.title)} chars): \"{p.title[:55]}\""))

    # ── Meta description ──────────────────────────────────────────────────────
    desc = p.metas.get("description", "")
    if not desc:
        issues.append(("critical", "Meta description mancante"))
    elif len(desc) < 70:
        issues.append(("warning", f"Meta description troppo corta ({len(desc)} chars)"))
    elif len(desc) > 165:
        issues.append(("warning", f"Meta description troppo lunga ({len(desc)} chars)"))
    else:
        issues.append(("ok", f"Meta description OK ({len(desc)} chars)"))

    # ── Canonical ─────────────────────────────────────────────────────────────
    if not p.canonical:
        issues.append(("critical", "Link canonical mancante"))
    else:
        issues.append(("ok", f"Canonical: {p.canonical}"))

    # ── H1 ────────────────────────────────────────────────────────────────────
    h1s = [h for h in p.headings if h[0] == "h1"]
    if not h1s:
        issues.append(("critical", "Nessun H1 trovato"))
    elif len(h1s) > 1:
        issues.append(("warning", f"Multipli H1 ({len(h1s)}): {[h[1][:40] for h in h1s]}"))
    else:
        t = h1s[0][1][:60]
        if len(t) < 5:
            issues.append(("warning", f"H1 troppo corto/generico: \"{t}\""))
        else:
            issues.append(("ok", f"H1 unico: \"{t}\""))

    # ── Heading hierarchy ─────────────────────────────────────────────────────
    prev_level = 0
    skip_jump = False
    for level_str, _ in p.headings:
        lvl = int(level_str[1])
        if prev_level and lvl > prev_level + 1:
            skip_jump = True
        prev_level = lvl
    if skip_jump:
        issues.append(("warning", "Gerarchia heading non sequenziale (salto di livello)"))

    # ── Open Graph ────────────────────────────────────────────────────────────
    og_required = ["og:title", "og:description", "og:image", "og:url", "og:type"]
    missing_og = [k for k in og_required if not p.metas.get(k)]
    if missing_og:
        issues.append(("warning", f"Open Graph mancanti: {', '.join(missing_og)}"))
    else:
        issues.append(("ok", "Open Graph completo"))

    # og:image dimensions
    if p.metas.get("og:image") and not p.metas.get("og:image:width"):
        issues.append(("warning", "og:image:width e og:image:height mancanti (raccomandati 1200x630)"))

    # ── Twitter Card ─────────────────────────────────────────────────────────
    tw_required = ["twitter:card", "twitter:title", "twitter:description", "twitter:image"]
    missing_tw = [k for k in tw_required if not p.metas.get(k)]
    if missing_tw:
        issues.append(("warning", f"Twitter Card mancanti: {', '.join(missing_tw)}"))
    else:
        issues.append(("ok", "Twitter Card completo"))

    # ── Hreflang ─────────────────────────────────────────────────────────────
    hreflang_links = [l for l in p.links if l.get("rel") == "alternate" and "hreflang" in l]
    langs_found = [l.get("hreflang") for l in hreflang_links]
    required_langs = {"it", "en", "fr", "es", "x-default"}
    missing_langs = required_langs - set(langs_found)
    if missing_langs:
        issues.append(("warning", f"Hreflang mancanti: {', '.join(missing_langs)}"))
    else:
        issues.append(("ok", "Hreflang completo (it/en/fr/es/x-default)"))

    # ── Schema.org ────────────────────────────────────────────────────────────
    if not p.schema_ld:
        issues.append(("warning", "Nessun JSON-LD Schema.org trovato"))
    else:
        types_found = []
        for raw in p.schema_ld:
            try:
                obj = json.loads(raw)
                # Handle both single object and array of objects
                items = obj if isinstance(obj, list) else [obj]
                for item in items:
                    if isinstance(item, dict):
                        t = item.get("@type", "?")
                        if isinstance(t, list): t = ", ".join(t)
                        types_found.append(t)
            except json.JSONDecodeError as e:
                issues.append(("warning", f"JSON-LD non valido: {e}"))
        if types_found:
            issues.append(("ok", f"Schema.org trovato: {', '.join(types_found)}"))

    # ── Immagini alt ─────────────────────────────────────────────────────────
    bad_imgs = []
    for img in p.images:
        # skip decorative images (aria-hidden="true" e alt="")
        if img["aria-hidden"] == "true" and img.get("alt") == "":
            continue
        if img["alt"] is None:
            bad_imgs.append(img["src"][:60])
        elif img["alt"] == "" and img["aria-hidden"] != "true":
            bad_imgs.append(f"{img['src'][:50]} (alt vuoto senza aria-hidden)")
    if bad_imgs:
        issues.append(("warning", f"{len(bad_imgs)} immagini senza alt: {bad_imgs[:3]}{'...' if len(bad_imgs)>3 else ''}"))
    else:
        issues.append(("ok", f"{len(p.images)} immagini — tutte con alt"))

    # ── Meta robots ──────────────────────────────────────────────────────────
    if not p.metas.get("robots"):
        issues.append(("warning", "Meta robots non specificato (default è index, follow)"))

    # ── favicon ──────────────────────────────────────────────────────────────
    favicon_links = [l for l in p.links if "icon" in l.get("rel","")]
    if not favicon_links:
        issues.append(("warning", "Favicon non trovata"))
    else:
        issues.append(("ok", "Favicon presente"))

    return issues, p, path


# ── Report ────────────────────────────────────────────────────────────────────
def print_report(results):
    total_critical = 0
    total_warnings = 0
    total_ok = 0

    print(f"\n{color('='*72, BOLD)}")
    print(f"{color('  SEO AUDIT — Badiani 1932 Brochure Site', BOLD+CYAN)}")
    print(f"{color('='*72, BOLD)}\n")

    for issues, parser, path in results:
        rel = path.relative_to(ROOT)
        crits  = [i for i in issues if i[0]=="critical"]
        warns  = [i for i in issues if i[0]=="warning"]
        oks    = [i for i in issues if i[0]=="ok"]

        status_icon = color("✗", RED) if crits else (color("⚠", YELLOW) if warns else color("✓", GREEN))
        print(f"{status_icon} {color(str(rel), BOLD)}")

        for _, msg in crits:
            print(f"   {color('🔴 CRITICO', RED)}  {msg}")
        for _, msg in warns:
            print(f"   {color('⚠  AVVISO', YELLOW)}  {msg}")
        for _, msg in oks:
            print(f"   {color('✅ OK', GREEN)}      {msg}")

        total_critical += len(crits)
        total_warnings += len(warns)
        total_ok       += len(oks)
        print()

    print(f"{color('─'*72, BOLD)}")
    print(f"  {color(f'🔴 Critici: {total_critical}', RED)}   "
          f"{color(f'⚠  Avvisi: {total_warnings}', YELLOW)}   "
          f"{color(f'✅ OK: {total_ok}', GREEN)}")
    print(f"{color('─'*72, BOLD)}\n")

    return total_critical, total_warnings


# ── Principale ────────────────────────────────────────────────────────────────
def main():
    html_files = sorted(ROOT.rglob("*.html"))
    # Exclude files inside _source, scripts, docs, node_modules
    html_files = [
        f for f in html_files
        if not any(part.startswith("_") or part in ("scripts","docs",".venv",".git","cloudflare")
                   for part in f.parts)
    ]

    results = []
    for f in html_files:
        results.append(analyze_file(f))

    crits, warns = print_report(results)

    print(f"  Pagine analizzate: {len(results)}")
    if crits == 0 and warns == 0:
        print(f"  {color('Perfetto! Nessun problema trovato.', GREEN+BOLD)}")
    elif crits == 0:
        print(f"  {color('Nessun problema critico.', GREEN)} Considera di risolvere gli avvisi.")
    else:
        print(f"  {color(f'Risolvi i {crits} problemi critici prima del deploy.', RED+BOLD)}")
    print()


if __name__ == "__main__":
    main()
