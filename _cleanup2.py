"""Remove remaining gelato.flavors/ingredients entries for discontinued flavors from STRINGS objects."""
import pathlib, re

FILE = pathlib.Path(__file__).parent / "b2b" / "index.html"
text = FILE.read_text(encoding="utf-8")

# Remove gelato.flavors.X and gelato.ingredients.X for vaniglia, banana
remove_keys = [
    "gelato.flavors.vaniglia",
    "gelato.flavors.banana",
    "gelato.ingredients.vaniglia",
    "gelato.ingredients.banana",
]

count = 0
for key in remove_keys:
    pattern = re.compile(r"^ *'" + re.escape(key) + r"':\s*'[^']*',?\s*\r?\n", re.MULTILINE)
    matches = pattern.findall(text)
    count += len(matches)
    text = pattern.sub("", text)

print(f"Removed {count} STRINGS lines")
FILE.write_text(text, encoding="utf-8")
print("Done")
