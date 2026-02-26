#!/usr/bin/env python3
"""
Add cookie banner translation strings to all 9 HTML pages' inline STRINGS objects.
Each page has STRINGS = { it: {...}, en: {...}, fr: {...}, es: {...} }.
"""
import re
import os

WORKSPACE = r'c:\Users\Mamabru\Documents\GitHub\Progetti\badiani1932B2B\badianibroshure'

# Files and their cookie-policy PATH prefix
FILES = {
    'index.html': '',
    'cookie-policy.html': '',
    'privacy.html': '',
    'b2b/index.html': '../',
    'magazine/index.html': '../',
    'eventi/index.html': '../',
    'eventi/evento-esterno/index.html': '../../',
    'eventi/saletta-privata-tosinghi/index.html': '../../',
    'eventi/speciale-aziende/index.html': '../../',
}

def get_cookie_strings(path_prefix):
    """Return dict of lang -> list of cookie key-value lines to insert."""
    return {
        'it': [
            f"          'cookie.aria': 'Informativa cookie',",
            f"          'cookie.text': 'Questo sito utilizza cookie tecnici per garantire il corretto funzionamento. <a href=\"{path_prefix}cookie-policy.html\">Maggiori informazioni</a>',",
            f"          'cookie.accept': 'Accetto',",
            f"          'cookie.link': 'Cookie Policy',",
        ],
        'en': [
            f"          'cookie.aria': 'Cookie notice',",
            f"          'cookie.text': 'This site uses technical cookies to ensure proper functioning. <a href=\"{path_prefix}cookie-policy.html\">More information</a>',",
            f"          'cookie.accept': 'Accept',",
            f"          'cookie.link': 'Cookie Policy',",
        ],
        'fr': [
            f"          'cookie.aria': 'Avis sur les cookies',",
            f"          'cookie.text': 'Ce site utilise des cookies techniques pour garantir son bon fonctionnement. <a href=\"{path_prefix}cookie-policy.html\">Plus d\\'informations</a>',",
            f"          'cookie.accept': 'Accepter',",
            f"          'cookie.link': 'Cookie Policy',",
        ],
        'es': [
            f"          'cookie.aria': 'Aviso de cookies',",
            f"          'cookie.text': 'Este sitio utiliza cookies t\\u00e9cnicas para garantizar el correcto funcionamiento. <a href=\"{path_prefix}cookie-policy.html\">M\\u00e1s informaci\\u00f3n</a>',",
            f"          'cookie.accept': 'Aceptar',",
            f"          'cookie.link': 'Cookie Policy',",
        ],
    }


def find_strings_block(content):
    """Find the STRINGS = { ... }; block using brace-matching."""
    match = re.search(r'(?:const|var)\s+STRINGS\s*=\s*\{', content)
    if not match:
        return None, None
    start = match.start()
    # Find matching closing brace
    depth = 0
    i = match.end() - 1  # position of the opening {
    while i < len(content):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                # Find the semicolon after
                end = i + 1
                while end < len(content) and content[end] in ' \t\n;':
                    end += 1
                return start, end
        i += 1
    return start, len(content)


def find_lang_sections(content, strings_start, strings_end):
    """
    Find each language section within the STRINGS block.
    Returns dict of lang -> (section_start, section_end) where section_end is the closing }
    """
    block = content[strings_start:strings_end]
    langs = {}
    # Find each lang declaration: e.g. "it: {" or "en: {"
    for lang in ['it', 'en', 'fr', 'es']:
        pattern = re.compile(r'\b' + lang + r'\s*:\s*\{')
        match = pattern.search(block)
        if not match:
            continue
        # Find the matching closing } for this lang section
        brace_start = match.end() - 1  # position of {
        depth = 0
        i = brace_start
        while i < len(block):
            if block[i] == '{':
                depth += 1
            elif block[i] == '}':
                depth -= 1
                if depth == 0:
                    langs[lang] = (strings_start + brace_start, strings_start + i)
                    break
            i += 1
    return langs


def insert_cookie_keys(content, filepath, path_prefix):
    """Insert cookie translation keys into each language section."""
    strings_start, strings_end = find_strings_block(content)
    if strings_start is None:
        print(f"  ERROR: Could not find STRINGS block in {filepath}")
        return content, False

    lang_sections = find_lang_sections(content, strings_start, strings_end)
    if len(lang_sections) < 4:
        print(f"  WARNING: Found only {len(lang_sections)} language sections in {filepath}")

    cookie_strings = get_cookie_strings(path_prefix)

    # Process languages in reverse order of position so insertions don't shift later positions
    sorted_langs = sorted(lang_sections.items(), key=lambda x: x[1][1], reverse=True)

    modified = False
    for lang, (sect_start, close_brace_pos) in sorted_langs:
        if lang not in cookie_strings:
            continue

        # Check if cookie keys already exist
        section_text = content[sect_start:close_brace_pos]
        if "'cookie.aria'" in section_text or '"cookie.aria"' in section_text:
            print(f"  SKIP {lang}: cookie keys already present")
            continue

        # Find the last key-value line before the closing brace
        # Look backwards from close_brace_pos to find the last non-whitespace line
        before_close = content[:close_brace_pos]
        # Find the last newline before closing brace
        last_nl = before_close.rfind('\n', sect_start, close_brace_pos)
        if last_nl == -1:
            last_nl = sect_start

        # Check if the last line before } ends with a comma; if not, add one
        last_line = content[last_nl:close_brace_pos].strip()
        
        # Build insertion text
        lines_to_insert = cookie_strings[lang]
        insertion = '\n' + '\n'.join(lines_to_insert)
        
        # If the last key line doesn't end with comma, we need to add one
        # Find the actual last key line (not just whitespace)
        search_back = content[:close_brace_pos].rstrip()
        if search_back and not search_back.endswith(','):
            # Add a comma after the last existing value
            pos = len(search_back)
            content = content[:pos] + ',' + insertion + '\n' + content[close_brace_pos:]
        else:
            content = content[:close_brace_pos] + insertion + '\n' + content[close_brace_pos:]

        modified = True
        print(f"  OK {lang}: inserted cookie keys")

        # Recalculate positions since content changed
        strings_start_new, strings_end_new = find_strings_block(content)
        if strings_start_new is not None:
            lang_sections = find_lang_sections(content, strings_start_new, strings_end_new)
            sorted_langs_remaining = [(l, p) for l, p in sorted(lang_sections.items(), key=lambda x: x[1][1], reverse=True) if l != lang and any(ll == l for ll, _ in sorted_langs[sorted_langs.index((lang, (sect_start, close_brace_pos)))+1:])]

    return content, modified


def process_file(rel_path, path_prefix):
    filepath = os.path.join(WORKSPACE, rel_path.replace('/', os.sep))
    print(f"\nProcessing: {rel_path}")

    if not os.path.exists(filepath):
        print(f"  ERROR: File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to process all 4 languages one at a time, recalculating positions each time
    cookie_strings = get_cookie_strings(path_prefix)
    
    any_modified = False
    for lang in ['es', 'fr', 'en', 'it']:  # Process in reverse doc order (es last in file → first to process)
        strings_start, strings_end = find_strings_block(content)
        if strings_start is None:
            print(f"  ERROR: Could not find STRINGS block")
            break

        lang_sections = find_lang_sections(content, strings_start, strings_end)
        if lang not in lang_sections:
            print(f"  SKIP {lang}: section not found")
            continue

        sect_start, close_brace_pos = lang_sections[lang]
        section_text = content[sect_start:close_brace_pos]
        
        if "'cookie.aria'" in section_text or '"cookie.aria"' in section_text:
            print(f"  SKIP {lang}: cookie keys already present")
            continue

        # Build insertion
        lines_to_insert = cookie_strings[lang]
        insertion = '\n'.join(lines_to_insert)

        # Check if last line before closing brace ends with comma
        before_brace = content[:close_brace_pos].rstrip()
        if before_brace.endswith(','):
            # Just insert after the comma
            content = content[:close_brace_pos] + '\n' + insertion + '\n' + content[close_brace_pos:]
        else:
            # Add comma to last line, then insert
            # Find position of last non-whitespace char before closing brace
            stripped_pos = len(before_brace)
            content = content[:stripped_pos] + ',\n' + insertion + '\n' + content[close_brace_pos:]

        any_modified = True
        print(f"  OK {lang}: inserted cookie keys")

    if any_modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  SAVED: {rel_path}")
    else:
        print(f"  NO CHANGES: {rel_path}")

    return any_modified


def main():
    print("=" * 60)
    print("Adding cookie banner translation strings to HTML pages")
    print("=" * 60)

    results = {}
    for rel_path, path_prefix in FILES.items():
        success = process_file(rel_path, path_prefix)
        results[rel_path] = success

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for path, ok in results.items():
        status = "OK" if ok else "SKIPPED/ERROR"
        print(f"  {status}: {path}")


if __name__ == '__main__':
    main()
