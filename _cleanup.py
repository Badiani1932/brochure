"""One-time cleanup script for b2b/index.html — remove discontinued flavors from i18n data."""
import pathlib, re

FILE = pathlib.Path(__file__).parent / "b2b" / "index.html"
text = FILE.read_text(encoding="utf-8")

# Keys to remove as full lines (each is an id-based key in descriptions or allergens)
remove_keys = [
    "cremino-al-pistacchio",
    "dubai-chocolate",
    "banana",
    "vaniglia",
    "sorbetto-cioccolato-venezuela",
    "sorbetto-tropical-summer",
]

count = 0
for key in remove_keys:
    # Match full line:   'key': '...', (with optional trailing comma)
    pattern = re.compile(r"^ *'" + re.escape(key) + r"':\s*'[^']*',?\s*\r?\n", re.MULTILINE)
    matches = pattern.findall(text)
    count += len(matches)
    text = pattern.sub("", text)
    
print(f"Removed {count} lines for discontinued keys")

# Update fondente description in FR desc section
# Old: 'fondente': 'Sorbet au chocolat noir monorigine 72%'
# New: 'fondente': 'Sorbet au chocolat noir monorigine du Venezuela, 72%'
old_fr = "'fondente': 'Sorbet au chocolat noir monorigine 72%'"
new_fr = "'fondente': 'Sorbet au chocolat noir monorigine du Venezuela, 72%'"
if old_fr in text:
    text = text.replace(old_fr, new_fr)
    print("Updated FR fondente description")
else:
    print("FR fondente description already updated or not found")

FILE.write_text(text, encoding="utf-8")
print("File saved successfully")
