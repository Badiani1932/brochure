# Gestione Asset e Immagini

> Allegare questo file quando si lavora su: aggiunta foto, ottimizzazione immagini, favicon, video, asset management.

---

## Formato Immagini

- **Primario**: WebP (compressione moderna, ~30-50% più leggero di JPG)
- **Fallback**: PNG per icone/loghi, JPG per vecchie istanze
- **Generazione**: Script Python per ottimizzazione batch e creazione thumbnail

---

## Struttura Cartelle Immagini

```text
assets/
├── gelato/           # 27 cartelle × 3 immagini = ~81 file WebP
├── images/
│   ├── branding/     # Logo, favicon (favicon.webp, favicon.ico, apple-touch-icon.png)
│   ├── categories/   # Immagini categorie B2B (vasche.webp, torte.webp, ecc.)
│   ├── eventi/       # Foto hero eventi + galleria
│   ├── torte/        # Foto torte prodotto
│   ├── vasche/       # Foto vasche gelato
│   ├── pezziduri/    # Foto gelati stecco/biscotto
│   ├── coni-coppette/# Foto coni e coppette
│   ├── contenitori/  # Foto contenitori
│   ├── accessori/    # Foto accessori
│   └── rassegna-stampa/ # Thumbnail articoli magazine
└── video/            # Video hero (MP4)
```

---

## Favicon

Il favicon usa la "B" di Badiani (`logo-b-white.png`) invece del logo completo.
File generati da sorgente 1248×1260 RGBA:

| File | Dimensione | Uso |
| ------ | ----------- | ----- |
| `favicon.webp` | 64×64, ~1.1 KB | Browser moderni (WebP) |
| `favicon.ico` | 32×32, ~4.8 KB | Fallback universale |
| `apple-touch-icon.png` | 180×180, ~17 KB | iOS home screen |
| `favicon-32.png` | 32×32, ~4.8 KB | Fallback PNG |

Ogni pagina HTML include:

```html
<link rel="icon" href=".../favicon.ico" sizes="32x32" />
<link rel="icon" href=".../favicon.webp" type="image/webp" />
<link rel="apple-touch-icon" href=".../apple-touch-icon.png" />
```

---

## Ottimizzazione

- **Above-fold preload**: `<link rel="preload" as="image" href="...">` per immagini hero
- **Font preload**: `<link rel="preload" as="font" ...>` per SuperGroteskB
- **Lazy loading**: Immagini sotto la fold caricate on-demand
- **Thumbnail**: Script `make_gelato_thumbs.py` genera versioni 420px per galleria veloce

---

## Regola Ottimizzazione Immagini

**Tutte le immagini fornite devono essere ottimizzate prima dell'inserimento:**

| Tipo | Formato | Dimensione max | Qualità |
| ------ | --------- | --------------- | ---------- |
| Hero/sfondo | WebP | 1800px lato lungo | 72-80 |
| Prodotto/dettaglio | WebP | 1200px lato lungo | 72-80 |
| Thumbnail/card | WebP | 420px larghezza | 80 |
| Favicon | WebP + ICO | 64px / 32px | 85 |
| Apple Touch Icon | PNG | 180×180 | ottimizzato |

Script disponibili per batch: `scripts/optimize_b2b_modal_images.py`, `scripts/make_gelato_thumbs.py`

---

## Script di Ottimizzazione

### Python Scripts (`scripts/`)

| Script | Scopo | Input | Output |
| -------- | ------- | ------- | -------- |
| `make_gelato_thumbs.py` | Genera thumbnail 420px per gusti gelato | `assets/gelato/*/` | `*-thumb.webp` (quality 80) |
| `optimize_b2b_modal_images.py` | Converti PNG/JPG → WebP ottimizzato | Cartelle prodotti | WebP (hero: 1800px, default: 1200px, quality 72) |
| `optimize_detail_images.py` | Ottimizza immagini dettaglio | Cartelle specifiche | WebP ottimizzato |

### Come Usare

```bash
# Attivare il virtual environment
.venv\Scripts\Activate.ps1

# Generare thumbnail gusti
python scripts/make_gelato_thumbs.py

# Ottimizzare immagini B2B
python scripts/optimize_b2b_modal_images.py
```

---

## Asset Orfani (da pulire)

| Asset | Motivo |
| ------- | -------- |
| `assets/i18n.js` | Sostituito da `src/i18n/i18n.js` |
| `pdf_extracted/` (~53 immagini) | Estratte da PDF, mai usate nel sito |
| `assets/extracted/brochure-italia/` (~28 pagine) | Estratte, inutilizzate |
| `foto_torte/` (PNG) | Sostituite da `foto_torte2/` (WebP) |
