"""Batch-optimize gelato PNG images to WebP and generate thumbnails."""
import os
from PIL import Image

BASE = os.path.join(os.path.dirname(__file__), '..', 'assets', 'gelato')

# (folder, source_png, target_webp)
TASKS = [
    # Buontalenti
    ('Buontalenti', 'buontalenti.png', 'buontalenti.webp'),
    ('Buontalenti', 'buontalenti - dettaglio.png', 'buontalenti-2.webp'),
    # Buontalenti Caramello (only main)
    ('Buontalenti Caramello', 'caramello.png', 'buontalenti_caramello.webp'),
    # Buontalenti Delattosato
    ('Buontalenti Delattosato', 'buontalenti delattosato.png', 'buontalenti_delattosato.webp'),
    ('Buontalenti Delattosato', 'buontalenti delattosato - dettaglio.png', 'buontalenti_delattosato-2.webp'),
    # Caffè
    ('Caffè', 'caffè.png', 'caffè.webp'),
    ('Caffè', 'caffè- dettaglio.png', 'caffè-2.webp'),
    # Cheesecake Frutti Rossi
    ('Cheesecake Frutti Rossi', 'cheese cake.png', 'cheesecake_fruttirossi.webp'),
    ('Cheesecake Frutti Rossi', 'cheese cake - dettaglio.png', 'cheesecake_fruttirossi-2.webp'),
    # Fondente
    ('Fondente', 'fondente.png', 'fondente.webp'),
    ('Fondente', 'fondente - dettaglio.png', 'fondente-2.webp'),
    # Fragola
    ('Fragola', 'fragola.png', 'fragola.webp'),
    ('Fragola', 'fragola - dettaglio.png', 'fragola-2.webp'),
    # Malaga
    ('Malaga', 'malaga.png', 'malaga.webp'),
    ('Malaga', 'malaga- dettaglio .png', 'malaga-2.webp'),
    # Stracciatella alla Menta (NEW)
    ('STRACCIATELLA ALLA MENTA', 'stacciatella alla menta.png', 'stracciatella_menta.webp'),
    ('STRACCIATELLA ALLA MENTA', 'stacciatella alla menta - dettaglio.png', 'stracciatella_menta-2.webp'),
]

MAX_PX = 1200
QUALITY = 78
THUMB_PX = 420
THUMB_QUALITY = 80


def optimize(src_path, dst_path, max_px, quality):
    img = Image.open(src_path)
    w, h = img.size
    orig = f"{w}x{h}"

    if max(w, h) > max_px:
        ratio = max_px / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    img.save(dst_path, 'WEBP', quality=quality, method=6)
    return orig, f"{img.size[0]}x{img.size[1]}", os.path.getsize(dst_path)


def main():
    total_saved = 0

    for folder, src_name, dst_name in TASKS:
        src_path = os.path.join(BASE, folder, src_name)
        dst_path = os.path.join(BASE, folder, dst_name)

        if not os.path.exists(src_path):
            print(f"  SKIP (missing): {folder}/{src_name}")
            continue

        src_kb = os.path.getsize(src_path) // 1024
        orig, final, dst_bytes = optimize(src_path, dst_path, MAX_PX, QUALITY)
        dst_kb = dst_bytes // 1024
        saved = src_kb - dst_kb
        total_saved += saved
        print(f"  OK  {folder}/{dst_name}  {orig}->{final}  {src_kb}KB->{dst_kb}KB  (-{saved}KB)")

        # Generate thumbnail for main (non-detail) images
        if not dst_name.endswith('-2.webp'):
            thumb_name = dst_name.replace('.webp', '-thumb.webp')
            thumb_path = os.path.join(BASE, folder, thumb_name)
            _, tfinal, tbytes = optimize(src_path, thumb_path, THUMB_PX, THUMB_QUALITY)
            tkb = tbytes // 1024
            print(f"  OK  {folder}/{thumb_name}  ->{tfinal}  {tkb}KB (thumb)")

    print(f"\nTotal saved: {total_saved}KB ({total_saved//1024}MB)")


if __name__ == '__main__':
    main()
