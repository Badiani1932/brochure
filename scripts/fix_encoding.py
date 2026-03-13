#!/usr/bin/env python3
"""
fix_encoding.py — Corregge il Mojibake UTF-8→Windows-1252 nei file HTML.

Pattern: un file UTF-8 originale è stato aperto come Windows-1252,
re-salvato, generando sequenze come â€" al posto di —, Ã© al posto di é, ecc.

Fix: rimpiazza ogni sequenza corrotta con il carattere Unicode corretto.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Mappa dei rimpiazzi: (stringa_corrotta → stringa_corretta)
# Generata applicando la logica: bytes.encode('windows-1252').decode('utf-8')
# Uso escaping Unicode per evitare problemi col parser Python.

def _u(*codepoints):
    return "".join(chr(c) for c in codepoints)

REPLACEMENTS = [
    # Punteggiatura tipografica
    (_u(0xE2, 0x20AC, 0x201D),  "\u2014"),   # â€" → — em dash U+2014
    (_u(0xE2, 0x20AC, 0x201C),  "\u201C"),   # â€œ → " left double quote U+201C
    (_u(0xE2, 0x20AC, 0x2026),  "\u2026"),   # â€¦ → … ellipsis U+2026
    (_u(0xE2, 0x20AC, 0x2122),  "\u2122"),   # â€¢ → ™ trademark (raro)
    (_u(0xE2, 0x20AC, 0x2019),  "\u2019"),   # â€™ → ' right single quote U+2019
    (_u(0xE2, 0x20AC, 0x2018),  "\u2018"),   # â€˜ → ' left single quote U+2018
    (_u(0xE2, 0x20AC, 0x2022),  "\u2022"),   # â€¢ → • bullet U+2022
    (_u(0xE2, 0x20AC, 0x2013),  "\u2013"),   # â€" → – en dash U+2013
    # Lettere accentate minuscole
    (_u(0xC3, 0xA9),  "\u00E9"),   # Ã© → é
    (_u(0xC3, 0xA8),  "\u00E8"),   # Ã¨ → è
    (_u(0xC3, 0xAA),  "\u00EA"),   # Ãª → ê
    (_u(0xC3, 0xA0),  "\u00E0"),   # Ã  → à
    (_u(0xC3, 0xAF),  "\u00EF"),   # Ã¯ → ï
    (_u(0xC3, 0xAD),  "\u00ED"),   # Ã­ → í
    (_u(0xC3, 0xAC),  "\u00EC"),   # Ã¬ → ì
    (_u(0xC3, 0xAE),  "\u00EE"),   # Ã® → î
    (_u(0xC3, 0xB3),  "\u00F3"),   # Ã³ → ó
    (_u(0xC3, 0xB2),  "\u00F2"),   # Ã² → ò
    (_u(0xC3, 0xB4),  "\u00F4"),   # Ã´ → ô
    (_u(0xC3, 0xB9),  "\u00F9"),   # Ã¹ → ù
    (_u(0xC3, 0xBA),  "\u00FA"),   # Ãº → ú
    (_u(0xC3, 0xBB),  "\u00FB"),   # Ã» → û
    (_u(0xC3, 0xBC),  "\u00FC"),   # Ã¼ → ü
    (_u(0xC3, 0xA7),  "\u00E7"),   # Ã§ → ç
    (_u(0xC3, 0xB1),  "\u00F1"),   # Ã± → ñ
    # Lettere accentate maiuscole
    (_u(0xC3, 0x89),  "\u00C9"),   # Ã‰ → É
    (_u(0xC3, 0x88),  "\u00C8"),   # Ãˆ → È
    (_u(0xC3, 0x80),  "\u00C0"),   # Ã€ → À
    (_u(0xC3, 0x93),  "\u00D3"),   # Ã" → Ó
    (_u(0xC3, 0x92),  "\u00D2"),   # Ã' → Ò
    (_u(0xC3, 0x87),  "\u00C7"),   # Ã‡ → Ç
    (_u(0xC3, 0x91),  "\u00D1"),   # Ã' → Ñ
    # Simboli
    (_u(0xE2, 0x82, 0xAC), "\u20AC"),   # â‚¬ → €
    (_u(0xC2, 0xA9),  "\u00A9"),   # Â© → ©
    (_u(0xC2, 0xAE),  "\u00AE"),   # Â® → ®
    (_u(0xC2, 0xB0),  "\u00B0"),   # Â° → °
    (_u(0xC2, 0xB7),  "\u00B7"),   # Â· → ·
    (_u(0xC2, 0xBB),  "\u00BB"),   # Â» → »
    (_u(0xC2, 0xAB),  "\u00AB"),   # Â« → «
]

# File da correggere (quelli con encoding corrotto)
TARGET_FILES = [
    "cookie-policy.html",
    "privacy.html",
    "eventi/evento-esterno/index.html",
    "eventi/saletta-privata-tosinghi/index.html",
]


def fix_file(path: Path) -> int:
    """Corregge il file e restituisce il numero di rimpiazzi effettuati."""
    original = path.read_text(encoding="utf-8")
    fixed = original
    total = 0
    for bad, good in REPLACEMENTS:
        count = fixed.count(bad)
        if count:
            fixed = fixed.replace(bad, good)
            total += count
            print(f"  {repr(bad)} → {repr(good)}: {count} occorrenze")
    if total:
        path.write_text(fixed, encoding="utf-8")
        print(f"  ✅ Salvato: {path.relative_to(ROOT)} ({total} rimpiazzi)")
    else:
        print(f"  ✓ Nessuna correzione necessaria: {path.relative_to(ROOT)}")
    return total


def main():
    print("=== Fix Encoding Mojibake — Badiani 1932 ===\n")
    grand_total = 0
    for rel in TARGET_FILES:
        path = ROOT / rel
        if not path.exists():
            print(f"  ⚠ File non trovato: {rel}")
            continue
        print(f"→ {rel}")
        grand_total += fix_file(path)
        print()
    print(f"Totale rimpiazzi: {grand_total}")


if __name__ == "__main__":
    main()
