# Badiani 1932 — Brochure Digitale (Eventi & B2B)

> Sito web brochure premium per **Badiani 1932**, storica gelateria artigianale fiorentina.
> Il sito serve come piattaforma B2B e per eventi aziendali — non è un e-commerce né un sito consumer.

**Live URL**: `https://www.badiani1932.com/`
**Repository**: `Badiani1932/badianibroshure` (branch: `main`)

> **Regola operativa**: Tutte le immagini fornite devono essere **ottimizzate per il web** prima di essere inserite nel sito (ridimensionamento, conversione WebP, compressione).

---

## Indice

1. [Panoramica Progetto](#panoramica-progetto)
2. [Stack Tecnologico](#stack-tecnologico)
3. [Struttura del Repository](#struttura-del-repository)
4. [Mappa delle Pagine](#mappa-delle-pagine)
5. [Architettura del Design](#architettura-del-design)
6. [Sistema i18n (Internazionalizzazione)](#sistema-i18n-internazionalizzazione)
7. [Catalogo Gelato (Data Layer)](#catalogo-gelato-data-layer)
8. [Gestione Asset e Immagini](#gestione-asset-e-immagini)
9. [Form di Contatto e API](#form-di-contatto-e-api)
10. [SEO e Indicizzazione](#seo-e-indicizzazione)
11. [Conformità Legale (GDPR)](#conformità-legale-gdpr)
12. [Accessibilità (a11y)](#accessibilità-a11y)
13. [Responsive Design e Breakpoint](#responsive-design-e-breakpoint)
14. [Script di Utilità](#script-di-utilità)
15. [Problemi Noti e Debito Tecnico](#problemi-noti-e-debito-tecnico)
16. [TODO e Funzionalità Pianificate](#todo-e-funzionalità-pianificate)
17. [Guida per Modifiche Future](#guida-per-modifiche-future)

---

## Panoramica Progetto

Badiani 1932 è una gelateria artigianale fondata a Firenze nel 1932. Questo sito web funziona come **brochure digitale interattiva** per due target principali:

| Target | Percorso | Scopo |
|--------|----------|-------|
| **Clienti Eventi** | `/ → /eventi/ → (sottopagine)` | Prenotare eventi privati, catering esterno, eventi aziendali |
| **Partner B2B** | `/ → /b2b/` | Esplorare catalogo prodotti, gusti, formati, allergeni — con form contatto |
| **Media/Stampa** | `/ → /magazine/` | Rassegna stampa e menzioni nei media |

### Flussi Utente

```
EVENTI:
Homepage → Hub Eventi → Saletta Privata / Evento Esterno / Speciale Aziende
                      → Selezione pacchetto → Modale dettagli → Form contatto → Email

B2B:
Homepage → Catalogo B2B → Navigazione categorie → Click prodotto → Modale dettagli
                        → Form contatto → Email

BRAND:
Homepage (storia + timeline) → Magazine (rassegna stampa) → Eventi/B2B
```

---

## Stack Tecnologico

| Livello | Tecnologia | Note |
|---------|-----------|------|
| **Frontend** | HTML5, CSS3, JavaScript vanilla | Nessun framework (React, Vue, etc.) |
| **CSS** | Custom Properties + `clamp()` + Grid/Flexbox | No Bootstrap, Tailwind, etc. |
| **Font** | SuperGrotesk (4 varianti custom `@font-face`) | File in `assets/fonts/` |
| **Immagini** | WebP (primario) + PNG/JPG fallback | ~300+ immagini |
| **Dati** | JS statico (`gelatoFlavors.js`) | Nessun CMS o database |
| **i18n** | 4 lingue (IT, EN, FR, ES) | Inline `STRINGS` + modulo ES6 |
| **API** | Cloudflare Worker (serverless) | Per invio email form contatto |
| **Email** | Gmail API con OAuth2 refresh token | Via Cloudflare Worker |
| **Hosting** | Sito statico (GitHub Pages / server) | + Worker su Cloudflare |
| **VCS** | Git | Repository GitHub |

### Dipendenze Esterne

Il sito è **completamente autocontenuto** — nessuna dipendenza esterna CDN, nessun npm, nessun framework JS.

Le uniche connessioni esterne sono:
- `https://badianiapiwebmail.marco-bruzzi.workers.dev/send` — API form contatto
- Link esterni nella pagina `/magazine/` verso articoli di stampa

---

## Struttura del Repository

```
badianibroshure/
│
├── index.html                          # Homepage principale
├── cookie-policy.html                  # Policy cookie (GDPR)
├── privacy.html                        # Informativa privacy (GDPR)
├── robots.txt                          # Regole crawler
├── sitemap.xml                         # Mappa del sito XML
│
├── assets/
│   ├── badiani-common.css              # ★ Foglio stile condiviso (tutti i componenti globali)
│   ├── i18n.js                         # ⚠ i18n legacy (NON USATO — orfano)
│   ├── fonts/                          # Font custom SuperGrotesk (woff, woff2, otf)
│   ├── gelato/                         # 27 cartelle gusto (3 immagini ciascuna)
│   │   ├── Buontalenti/
│   │   ├── Pistacchio/
│   │   ├── DUBAI CHOCOLATE/
│   │   └── ... (27 cartelle)
│   ├── images/
│   │   ├── branding/                   # Logo, sfondi brand
│   │   ├── categories/                 # Immagini categorie B2B (es. gusti.webp, vasche.webp, torte.webp, coni-coppette.webp, contenitori.webp, accessori.webp)
│   │   ├── eventi/                     # Foto eventi + galleria
│   │   ├── torte/                      # Foto torte
│   │   ├── vasche/                     # Foto vasche gelato
│   │   ├── pezziduri/                  # Foto pezzi duri
│   │   ├── coni-coppette/              # Foto coni e coppette
│   │   ├── contenitori/                # Foto contenitori
│   │   ├── accessori/                  # Foto accessori
│   │   ├── rassegna-stampa/            # Immagini articoli magazine
│   │   └── migrated/eventi/            # Foto eventi storici
│   ├── video/                          # Video hero/background
│   └── docs/                           # Documenti PDF (brochure, ecc.)
│
├── data/
│   └── gelatoFlavors.js                # ★ Dati catalogo gelato (27 gusti, allergeni, flag)
│
├── src/
│   └── i18n/
│       └── i18n.js                     # ★ Modulo i18n moderno (ES6 module, usato da B2B)
│
├── b2b/
│   └── index.html                      # ★ Pagina catalogo B2B (~2700 righe, la più grande)
│
├── eventi/
│   ├── index.html                      # Hub eventi (landing page eventi)
│   ├── saletta-privata-tosinghi/
│   │   └── index.html                  # Pacchetti Silver/Gold/Platinum
│   ├── evento-esterno/
│   │   └── index.html                  # Cool Box / Carretto / Vetrina
│   ├── speciale-aziende/
│   │   └── index.html                  # Eventi corporate personalizzati
│   ├── CT FIRENZE/                     # Assets evento specifico
│   └── foto eventi/                    # Galleria foto eventi
│       ├── Steve Madden MICAM/
│       └── Steve Madden Pitti/
│
├── magazine/
│   └── index.html                      # Rassegna stampa / "Dicono di Noi"
│
├── cloudflare/
│   ├── contact-api-worker.js           # ★ Worker Cloudflare per invio email
│   └── wrangler.toml                   # Configurazione deployment Worker
│
├── docs/
│   ├── IMPLEMENTATION-SUMMARY.md       # Changelog implementazione
│   ├── ASSET-AUDIT-REPORT.md           # Audit inventario asset
│   ├── CLOUDFLARE-WORKER-CONTACT-SETUP.md # Guida setup API contatto
│   ├── content-map-brochure-italia.md  # Mappa contenuti brochure → sito
│   └── REPO-CLEANUP-NOTES-2026-02-20.md # Note pulizia repository
│
├── scripts/
│   ├── make_gelato_thumbs.py           # Genera thumbnail gusti gelato
│   ├── optimize_b2b_modal_images.py    # Ottimizza immagini modali B2B (→ WebP)
│   ├── optimize_detail_images.py       # Ottimizza immagini dettaglio
│   ├── extract_docx_links.py           # Estrae link da file DOCX
│   ├── extract_docx_tables.py          # Estrae tabelle da file DOCX
│   └── fix-encoding.ps1               # Fix encoding caratteri
│
└── _source/
    ├── add_cookie_strings.py           # Inietta stringhe cookie in tutte le 9 pagine HTML
    ├── extract_pdf.py                  # Estrae immagini/testo da PDF brochure
    └── magazine.txt                    # URL articoli stampa (fonte dati magazine)
```

### Legenda

- ★ = File critico per il funzionamento del sito
- ⚠ = File problematico o deprecato

---

## Mappa delle Pagine

### Struttura di Navigazione

```
┌─────────────────────────────────────────────────┐
│                  HOMEPAGE (/)                    │
│  Hero video → Storia → Presenza Globale         │
│  → Scelta: [EVENTI] o [B2B]                     │
└──────┬────────────────────────┬──────────────────┘
       │                        │
       ▼                        ▼
┌──────────────┐        ┌──────────────┐
│  /eventi/    │        │    /b2b/     │
│  Hub Eventi  │        │  Catalogo    │
│  3 tipologie │        │  Prodotti    │
│  + Gelato Van│        │  + Form      │
└──┬───┬───┬───┘        └──────────────┘
   │   │   │
   ▼   ▼   ▼
┌────────────────────────────────────┐
│ /eventi/saletta-privata-tosinghi/  │  ← 3 pacchetti (Silver/Gold/Platinum)
│ /eventi/evento-esterno/            │  ← 3 soluzioni (Cool Box/Carretto/Vetrina)
│ /eventi/speciale-aziende/          │  ← Corporate personalizzato
└────────────────────────────────────┘

Pagine trasversali:
  /magazine/         → Rassegna stampa
  /cookie-policy.html → Policy cookie
  /privacy.html      → Informativa privacy
```

### Dettaglio per Pagina

| Pagina | URL | Contenuto Principale | LOC stimate |
|--------|-----|---------------------|-------------|
| **Homepage** | `/` | Hero video, storia timeline (1500→1960→oggi), presenza globale, scelta eventi/b2b | ~500 |
| **Hub Eventi** | `/eventi/` | Hero video, griglia 3 tipologie evento, sezione corporate, galleria foto, form contatto | ~400 |
| **Saletta Privata** | `/eventi/saletta-privata-tosinghi/` | 3 pacchetti con prezzo (Silver €20, Gold €30★, Platinum €40+), modali dettaglio menu | ~400 |
| **Evento Esterno** | `/eventi/evento-esterno/` | 3 soluzioni outdoor (Cool Box, Carretto, Vetrina), griglia specifiche, pricing | ~300 |
| **Speciale Aziende** | `/eventi/speciale-aziende/` | 5 feature cards, casi d'uso, CTA contatto | ~200 |
| **Catalogo B2B** | `/b2b/` | Griglia categorie (9), catalogo gusti dinamico (27), modali prodotto, form contatto | ~2700 |
| **Magazine** | `/magazine/` | Griglia articoli stampa (20+), link esterni | ~400 |
| **Cookie Policy** | `/cookie-policy.html` | Testo legale strutturato, tabella cookie, istruzioni browser | ~400 |
| **Privacy Policy** | `/privacy.html` | Informativa GDPR completa, basi giuridiche, diritti interessati | ~400 |

---

## Architettura del Design

### Design System

Il sito usa un design system coerente basato su:

#### Palette Colori (CSS Custom Properties)

```css
:root {
  --badiani-blue:   #1e398d;    /* Colore primario — topbar, titoli, CTA */
  --badiani-pink:   #f067a6;    /* Accento — hover, badge promosso, decorazioni */
  --badiani-yellow: #D8A200;    /* Accento secondario — highlights */
  --badiani-cyan:   #5B9AAD;    /* Accento terziario — step indicators */
  --badiani-gray:   #58595b;    /* Testo corpo */
  --bg-light:       #f8f8f8;    /* Sfondo pagina */
  --surface:        #ffffff;    /* Sfondo card/contenitori */
}
```

#### Spacing Scale

```css
:root {
  --space-xxl: 90px;    /* Sezioni principali */
  --space-xl:  72px;    /* Padding hero/sezioni */
  --space-lg:  48px;    /* Gap tra elementi */
  --space-md:  28px;    /* Padding interni */
}
```

#### Tipografia

| Font | Uso | File |
|------|-----|------|
| **SuperGroteskB** (Condensed Medium) | Titoli `h1, h2, h3`, hero text | `SuperGroteskB-CdMed.woff2/.woff` |
| **SuperGroteskA** (Regular) | Testo corpo, paragrafi | `SuperGroteskA-Rg[7511].woff2/.woff` |
| **SuperGroteskDigits** | Solo numeri 0-9 (unicode-range: U+0030-0039) | `SuperGroteskC-MedLF.otf` |
| **SuperGroteskC** (Full) | Elementi specifici che lo referenziano | `SuperGroteskC-MedLF.otf` |

- Titoli: `font-family: 'SuperGroteskDigits', 'SuperGroteskB', 'SuperGroteskA', sans-serif`
- Corpo: `font-family: 'SuperGroteskDigits', 'SuperGroteskA', 'SuperGroteskB', sans-serif`
- Tipografia fluida con `clamp()`: es. `font-size: clamp(28px, 3.6vw, 48px)`

#### Decorazione Titoli — `.title-accent`

Quadrato rosa decorativo dietro la prima lettera del titolo + linea sottile a destra.
Usa unità `em` per scalare proporzionalmente con il font-size del titolo.

```css
.title-accent::before {  /* Quadrato rosa */
  width: 0.52em; height: 0.52em;
  background: var(--badiani-pink);
}
.title-accent::after {   /* Linea decorativa */
  height: 1px;
  background: rgba(30, 57, 141, 0.12);
}
```

### Componenti Condivisi (in `badiani-common.css`)

| Componente | Classe | Descrizione |
|-----------|--------|-------------|
| **Topbar** | `.topbar` | Header sticky blu, logo + nav + selettore lingua + hamburger mobile |
| **Mobile Nav** | `.topbar__mobile-nav` | Overlay fullscreen con animazione slide-in |
| **Hamburger** | `.topbar__hamburger` | Icona animata ☰ ↔ ✕ |
| **Selettore Lingua** | `.topbar__select` | Dropdown custom con chevron SVG inline |
| **Footer** | `.site-footer` | Grid 4 colonne (brand, navigazione, servizi, legale) |
| **Cookie Banner** | `.cookie-banner` | Banner sticky bottom con accept + info |
| **Skip Link** | `.skip-link` | Link accessibilità (visibile solo su focus) |
| **Title Accent** | `.title-accent` | Decorazione quadrato rosa sui titoli |

### Pattern di Animazione

| Pattern | Proprietà | Durata |
|---------|----------|--------|
| **Page Reveal** | `opacity: 0 → 1` + `translateY(-16px → 0)` | 0.6s + stagger 0.04s-0.88s |
| **Card Hover** | `scale(1.06)` + brightness ridotta | 0.3s-0.8s `cubic-bezier(0.4, 0, 0.2, 1)` |
| **Nav Hover** | `translateY(-2px)` + sfondo rosa | 0.3s |
| **Modal Open** | `opacity: 0 → 1` + backdrop blur | 0.3s |
| **Reduced Motion** | Tutte le animazioni disabilitate | `@media (prefers-reduced-motion: reduce)` |

#### Category Cards (B2B)

Le category card nella pagina B2B usano lo stesso pattern visivo delle choice card della homepage:
- **Titoli in alto a sinistra** (`.category-title` dentro `.category-card__overlay` con `justify-content:flex-start`)
- **Descrizioni come CTA button** (`.category-cta` con freccia SVG, sfondo `--badiani-blue`, hover bianco)
- Al passaggio del mouse il bottone diventa bianco con testo blu e la freccia scorre a destra

### Pattern CSS Ricorrenti

```css
/* Full-bleed con overlay scuro */
background: url('immagine.webp') center/cover no-repeat;
filter: brightness(0.65);

/* Tipografia fluida */
font-size: clamp(min, preferred, max);

/* Grid responsive */
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));

/* Card con hover */
transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
&:hover { transform: translateY(-4px); }
```

### Pagine con CSS Inline

Ogni pagina HTML ha un blocco `<style>` con CSS specifico della pagina.
Lo stile condiviso è in `badiani-common.css`. Questa è un'area di **debito tecnico** —
idealmente gli stili specifici dovrebbero essere estratti in file CSS separati.

---

## Sistema i18n (Internazionalizzazione)

### Lingue Supportate

| Codice | Lingua |
|--------|--------|
| `it` | Italiano (default) |
| `en` | English |
| `fr` | Français |
| `es` | Español |

### Implementazione Attuale (Duale)

Esistono **due sistemi i18n** nel progetto:

#### 1. STRINGS Inline (usato da 8/9 pagine)

Ogni pagina HTML contiene un oggetto `STRINGS` con tutte le traduzioni inline:

```javascript
const STRINGS = {
  it: {
    hero_title: "Esperienze Badiani",
    hero_sub: "Gelato artigianale dal 1932...",
    // ...
  },
  en: { /* ... */ },
  fr: { /* ... */ },
  es: { /* ... */ }
};
```

Il selettore lingua (`.topbar__select`) aggiorna il DOM iterando sugli elementi con `data-i18n`:

```html
<h1 data-i18n="hero_title">Esperienze Badiani</h1>
```

La lingua è persistita in `localStorage` con chiave `badianiLang`.

#### 2. Modulo ES6 `src/i18n/i18n.js` (usato da B2B)

Modulo moderno con funzioni esportate:

```javascript
export function getLanguage()                    // → 'it'
export function setLanguage(lang)                // Salva + notifica subscribers
export function onLanguageChange(fn)             // Sottoscrizione reattiva
export function t(key, params)                   // Traduzione con parametri
export async function initI18n()                 // Carica dizionari JSON
```

Carica dizionari da `./locales/{locale}.json` (file JSON separati).
Usa pattern subscriber per aggiornamento reattivo.

#### 3. assets/i18n.js — DEPRECATO/ORFANO

File legacy, non importato da nessuna pagina. Da rimuovere in futuro.

### Persistenza Lingua

- **Storage**: `localStorage.getItem('badianiLang')`
- **Fallback**: Tenta `navigator.language`, altrimenti `'it'`
- **Sincronizzazione**: Ogni pagina legge la lingua corrente da localStorage all'avvio
- **Attributo HTML**: `<html lang="...">` viene aggiornato dinamicamente

---

## Catalogo Gelato (Data Layer)

### File: `data/gelatoFlavors.js`

Array di 27 oggetti gusto, esportato come modulo ES6.

### Struttura Dati per Gusto

```javascript
{
  id: "buontalenti",                                      // Identificativo unico
  nameKey: "flavor.buontalenti",                          // Chiave i18n
  label: "Buontalenti",                                   // Nome display
  seasons: ["tutti"],                                     // Stagionalità
  image: "../assets/gelato/Buontalenti/buontalenti.webp", // Immagine principale
  detailImage: "../assets/gelato/Buontalenti/buontalenti-2.webp", // Immagine dettaglio
  description: "Il nostro gusto iconico...",               // Descrizione IT
  allergensText: "Latte, uova",                           // Allergeni (testo)
  ingredients: [],                                        // Ingredienti (non compilato)
  allergens: [],                                          // Allergeni (array, non compilato)
  flags: {
    vegan: false,            // Vegano
    glutenFree: true,        // Senza glutine
    lactoseFree: false,      // Senza lattosio
    containsEggs: true,      // Contiene uova
    containsNuts: false,     // Contiene frutta a guscio
    containsAlcohol: false   // Contiene alcol
  },
  isTub: true                // Disponibile in vaschetta
}
```

### I 27 Gusti

| # | Gusto | Allergeni chiave | Flag speciali |
|---|-------|-----------------|---------------|
| 1 | Buontalenti | Latte, uova | Senza glutine |
| 2 | La Dolcevita | Latte, uova, frutta a guscio | — |
| 3 | Buontalenti al Pistacchio | Latte, uova, frutta a guscio | — |
| 4 | Buontalenti Caramello | Latte, uova, soia, glutine | — |
| 5 | Buontalenti all'Amarena | Latte, uova | Senza glutine |
| 6 | Buontalenti Delattosato | Uova | Senza lattosio, senza glutine |
| 7 | Buontalenti Fondente | Latte, uova, soia | — |
| 8 | Pistacchio | Latte, frutta a guscio | Senza glutine |
| 9 | Nocciola | Latte, frutta a guscio | Senza glutine |
| 10 | Cioccolato al Latte | Latte, soia | Senza glutine |
| 11 | Fondente | Soia | Vegano, senza glutine, senza lattosio |
| 12 | DUBAI CHOCOLATE | Latte, frutta a guscio, soia | — |
| 13 | Caramello Salato | Latte | Senza glutine |
| 14 | Cassandra | Latte, glutine, soia | — |
| 15 | Stracciatella | Latte, soia | Senza glutine |
| 16 | Caffè | Latte | Senza glutine |
| 17 | Malaga | Latte | Contiene alcol, senza glutine |
| 18 | Tiramisù | Latte, uova, glutine | Contiene alcol |
| 19-27 | Yogurt, Fragola, Mango, Limone, Lampone, Cocco, ecc. | Variabili | Alcuni vegani |

### Uso nel B2B

La pagina `b2b/index.html` importa i dati e genera dinamicamente:
- **Griglia gusti**: Cards con immagine + nome + badge allergeni
- **Modali prodotto**: Overlay fullscreen con dettaglio completo (foto, specifiche, allergeni, flag dietetici)
- **Filtri categoria**: 9 categorie (gelato, torte, vasche, pezziduri, coppette, cono, cialde, contenitori, accessori)

### Immagini Gusti

Ogni gusto ha 3 varianti immagine:
```
assets/gelato/{NomeGusto}/
├── {gusto}.webp          # Immagine principale (card)
├── {gusto}-2.webp        # Immagine dettaglio (modale)
└── {gusto}-thumb.webp    # Thumbnail (generata da script)
```

---

## Gestione Asset e Immagini

### Formato Immagini

- **Primario**: WebP (compressione moderna, ~30-50% più leggero di JPG)
- **Fallback**: PNG per icone/loghi, JPG per vecchie istanze
- **Generazione**: Script Python per ottimizzazione batch e creazione thumbnail

### Struttura Cartelle Immagini

```
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

### Favicon

Il favicon usa la "B" di Badiani (`logo-b-white.png`) invece del logo completo.
File generati da sorgente 1248×1260 RGBA:

| File | Dimensione | Uso |
|------|-----------|-----|
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

### Ottimizzazione

- **Above-fold preload**: `<link rel="preload" as="image" href="...">` per immagini hero
- **Font preload**: `<link rel="preload" as="font" ...>` per SuperGroteskB
- **Lazy loading**: Immagini sotto la fold caricate on-demand
- **Thumbnail**: Script `make_gelato_thumbs.py` genera versioni 420px per galleria veloce

### Regola Ottimizzazione Immagini

**Tutte le immagini fornite devono essere ottimizzate prima dell'inserimento:**

| Tipo | Formato | Dimensione max | Qualità |
|------|---------|---------------|----------|
| Hero/sfondo | WebP | 1800px lato lungo | 72-80 |
| Prodotto/dettaglio | WebP | 1200px lato lungo | 72-80 |
| Thumbnail/card | WebP | 420px larghezza | 80 |
| Favicon | WebP + ICO | 64px / 32px | 85 |
| Apple Touch Icon | PNG | 180×180 | ottimizzato |

Script disponibili per batch: `scripts/optimize_b2b_modal_images.py`, `scripts/make_gelato_thumbs.py`

### Asset Orfani (da pulire)

| Asset | Motivo |
|-------|--------|
| `assets/i18n.js` | Sostituito da `src/i18n/i18n.js` |
| `pdf_extracted/` (~53 immagini) | Estratte da PDF, mai usate nel sito |
| `assets/extracted/brochure-italia/` (~28 pagine) | Estratte, inutilizzate |
| `foto_torte/` (PNG) | Sostituite da `foto_torte2/` (WebP) |

---

## Form di Contatto e API

### Architettura

```
[Browser Form] --POST JSON--> [Cloudflare Worker] --OAuth2--> [Gmail API] --> Email
```

### Frontend (Form HTML)

Presente in: `/eventi/index.html`, `/b2b/index.html`

```javascript
// Payload inviato al worker
{
  source: "eventi-hub",        // Identificativo pagina
  formId: "ev-contact-form",   // ID form HTML
  subject: "Richiesta evento", // Oggetto email
  message: "...",              // Corpo messaggio
  fields: {                    // Campi strutturati
    nome: "...",
    email: "...",
    telefono: "...",
    azienda: "...",
    tipologia: "...",
    messaggio: "..."
  },
  structured: true
}
```

### Backend — `cloudflare/contact-api-worker.js`

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/health` | GET | Health check (`{ ok: true }`) |
| `/send` | POST | Riceve form, classifica, invia email |
| `/send` | OPTIONS | CORS preflight |

**Classificazione automatica** dei messaggi:
- Keyword "aziendale" → tag `[CORPORATE]`
- Keyword "evento" → tag `[EVENTI]`
- Keyword "b2b" → tag `[B2B]`
- Default → tag `[GENERAL]`

**Sicurezza**:
- Validazione origin (whitelist in env vars)
- Sanitizzazione subject (max 200 char, single-line)
- Pulizia body messaggio
- No dettagli interni negli errori al client
- Request ID per tracciamento

### Configurazione Worker (`wrangler.toml`)

```toml
name = "badiani-contact-api"
[vars]
ALLOWED_ORIGIN = "https://www.badiani1932.com,https://badiani1932.github.io"
MAIL_TO = "eventi@badiani1932.com"
MAIL_FROM = "eventi@badiani1932.com"
```

**Secret** (impostati via dashboard Cloudflare, mai nel codice):
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REFRESH_TOKEN`

### Troubleshooting Form

| Errore | Causa | Fix |
|--------|-------|-----|
| 403 | Origin non nella whitelist | Aggiornare `ALLOWED_ORIGIN` in wrangler.toml |
| 502 | Credenziali OAuth scadute/errate | Rinnovare `GOOGLE_REFRESH_TOKEN` nel dashboard |
| 404 | Path errato | Verificare endpoint `/send` |
| 500 | Config mancante | Verificare variabili env nel Worker |

---

## SEO e Indicizzazione

### Meta Tags (ogni pagina)

```html
<!-- Canonical -->
<link rel="canonical" href="https://www.badiani1932.com/{path}" />

<!-- Favicon (B logo) -->
<link rel="icon" href=".../favicon.ico" sizes="32x32" />
<link rel="icon" href=".../favicon.webp" type="image/webp" />
<link rel="apple-touch-icon" href=".../apple-touch-icon.png" />

<!-- Open Graph -->
<meta property="og:type" content="website" />
<meta property="og:title" content="Badiani 1932 — ..." />
<meta property="og:description" content="..." />
<meta property="og:image" content=".../logo.webp" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />

<!-- Hreflang (4 lingue + x-default) -->
<link rel="alternate" hreflang="it" href="..." />
<link rel="alternate" hreflang="en" href="..." />
<link rel="alternate" hreflang="fr" href="..." />
<link rel="alternate" hreflang="es" href="..." />
<link rel="alternate" hreflang="x-default" href="..." />
```

### Dati Strutturati

- **Schema.org BreadcrumbList** sulla homepage
- `<meta name="theme-color" content="#1e398d">`

### Sitemap (`sitemap.xml`)

7 pagine principali indicizzate + privacy e cookie policy.
Frequenza: mensile (pagine statiche), settimanale (magazine).

### Robots.txt

```
Allow: /                  # Tutto il contenuto pubblico
Disallow: /_source/       # Script sorgente
Disallow: /scripts/       # Script utility
Disallow: /docs/          # Documentazione interna
Disallow: /assets/docs/   # Documenti PDF
```

### Content Security Policy (CSP)

```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://badianiapiwebmail.marco-bruzzi.workers.dev;
  font-src 'self';
  frame-ancestors 'self';
  base-uri 'self'
" />
```

---

## Conformità Legale (GDPR)

### Cookie Policy (`cookie-policy.html`)

- **Cookie tecnici usati**:
  - `badianiLang` (localStorage, persistente) — preferenza lingua
  - `badianiCookieConsent` (localStorage, 12 mesi) — consenso cookie
- **Nessun cookie di**: analytics, marketing, profilazione, terze parti
- **Base giuridica**: Art. 122 D.Lgs. 196/2003 (aggiornato dal D.Lgs. 101/2018)
- **Banner cookie**: Componente `.cookie-banner` in ogni pagina

### Privacy Policy (`privacy.html`)

- **Titolare**: Sviluppo Gelato S.r.l. (Prato, Italia)
- **Dati raccolti**: Contatto, business B2B, navigazione, eventi, preferenze
- **Finalità**: Richieste contatto (24 mesi), preventivi eventi (24 mesi), B2B (24 mesi)
- **Basi giuridiche**: Art. 6.1.a (consenso), Art. 6.1.b (precontrattuale), Art. 6.1.f (legittimo interesse)
- **Trasferimenti**: Nessuno fuori dallo SEE
- **Diritti**: Accesso, rettifica, cancellazione (GDPR Art. 15-22)

### Traduzioni Legali

Entrambe le pagine legali sono tradotte nelle 4 lingue supportate (IT, EN, FR, ES) tramite oggetti `STRINGS` inline.

---

## Accessibilità (a11y)

### Implementato

| Feature | Dettaglio |
|---------|----------|
| **Skip Link** | `.skip-link` visibile solo su `:focus-visible` |
| **Focus Visible** | Outline 2px su tutti gli elementi interattivi |
| **Semantica HTML5** | `<header>`, `<main>`, `<footer>`, `<nav>`, `<article>` |
| **ARIA Labels** | Su campi form, bottoni, navigazione |
| **Reduced Motion** | `@media (prefers-reduced-motion: reduce)` disabilita animazioni |
| **Alt Text** | Immagini con attributo `alt` descrittivo |
| **Touch Targets** | `min-height: 44px` su tutti gli elementi interattivi (WCAG 2.5.5) |
| **Contrasto** | Testo bianco su `--badiani-blue` (#1e398d) = ratio ~8:1 |
| **Tap Highlight** | `-webkit-tap-highlight-color: transparent` per mobile |
| **Safe Area** | `env(safe-area-inset-*)` per dispositivi con notch |

### Da Migliorare

- Audit completo WCAG 2.1 AA non ancora eseguito
- Navigazione da tastiera nei modali (focus trap)
- Test con screen reader

---

## Responsive Design e Breakpoint

### Breakpoint

| Breakpoint | Target | Effetto Principale |
|-----------|--------|-------------------|
| `≤ 400px` | Smartphone piccolo | Topbar compatta, font ridotto |
| `≤ 500px` | Smartphone | Nav links più piccoli |
| `≤ 600px` | Mobile | Grid a 1 colonna, padding ridotto |
| `≤ 768px` | Tablet | Hamburger menu attivo, nav nascosta, grid 1-2 colonne |
| `≤ 900px` | Tablet grande | Nav ridimensionata |
| `> 768px` | Desktop | Layout completo, nav visibile, grid multi-colonna |

### Strategia

- **Mobile-first media queries** (`max-width`)
- **Tipografia fluida**: `clamp(min, preferred, max)` su tutti i testi
- **Grid responsive**: `repeat(auto-fit, minmax(280px, 1fr))`
- **Container queries**: Alcune card B2B usano `cqi` per sizing basato sul contenitore
- **Safe area insets**: Supporto per notch/barra home iOS

---

## Script di Utilità

### Python Scripts (`scripts/`)

| Script | Scopo | Input | Output |
|--------|-------|-------|--------|
| `make_gelato_thumbs.py` | Genera thumbnail 420px per gusti gelato | `assets/gelato/*/` | `*-thumb.webp` (quality 80) |
| `optimize_b2b_modal_images.py` | Converti PNG/JPG → WebP ottimizzato | Cartelle prodotti | WebP (hero: 1800px, default: 1200px, quality 72) |
| `optimize_detail_images.py` | Ottimizza immagini dettaglio | Cartelle specifiche | WebP ottimizzato |
| `extract_docx_links.py` | Estrae hyperlink da DOCX → JSON | File .docx | JSON con titolo + URL |
| `extract_docx_tables.py` | Estrae tabelle da DOCX | File .docx | Dati strutturati |
| `fix-encoding.ps1` | Fix encoding caratteri | File con encoding errato | File corretti |

### Source Scripts (`_source/`)

| Script | Scopo | Note |
|--------|-------|------|
| `add_cookie_strings.py` | Inietta stringhe cookie in tutte le 9 pagine HTML | Cerca `STRINGS = {...}`, aggiunge chiavi per lingua |
| `extract_pdf.py` | Estrae immagini/testo da PDF brochure | Usa PyMuPDF (fitz) |

### Come Usare gli Script

```bash
# Attivare il virtual environment
.venv\Scripts\Activate.ps1

# Generare thumbnail gusti
python scripts/make_gelato_thumbs.py

# Ottimizzare immagini B2B
python scripts/optimize_b2b_modal_images.py

# Iniettare stringhe cookie in tutte le pagine
python _source/add_cookie_strings.py
```

---

## Problemi Noti e Debito Tecnico

### ⚡ Troubleshooting Rapido VS Code

> **Prima di investigare qualsiasi anomalia visiva o di file in VS Code, prova queste soluzioni in ordine:**

| # | Sintomo | Soluzione immediata |
|---|---------|---------------------|
| 1 | Pagina appare con design vecchio/diverso nell'anteprima | **Riavvia VS Code** — la preview può rimanere in cache con versione obsoleta |
| 2 | File modificato ma le modifiche non sembrano applicate | Riavvia VS Code oppure `Developer: Reload Window` (Ctrl+Shift+P) |
| 3 | Git diff mostra caratteri strani (es. `┬«` invece di `®`) | Falso allarme — è solo il terminale PowerShell che non renderizza UTF-8; il file è corretto |
| 4 | Errori lint in file non toccati | Cache linter stantia — riavvia VS Code |
| 5 | Estensione non risponde o tool fallisce | Riavvia VS Code |

**Regola d'oro**: Se qualcosa sembra rotto ma git conferma che il file è identico a HEAD e il sito live funziona → **riavvia VS Code prima di fare qualsiasi modifica**.

---

### Problemi Critici

| # | Problema | Impatto | Fix Suggerito |
|---|---------|---------|---------------|
| 1 | File `.woff2` mancanti per SuperGroteskB/A | Font ~20% più pesanti (solo .woff caricati) | Verificare e copiare .woff2 se disponibili |
| 2 | Video mancanti (`inspiration/1220.mp4`, `videospesa.mp4`) | Player video rotto su pagine che li referenziano | Procurare o rimuovere riferimenti |

### Modifiche Recenti (Mar 2026)

| Data | Modifica |
|------|----------|
| 2026-03-13 | **Gelato — rimosse varianti mobile light**: eliminato il sistema di immagini `-2-light.webp` per mobile (27 file, ~1 MB). Tutti i dispositivi ora caricano la stessa immagine dettaglio `-2.webp`. Rimossa la funzione `getDetailImageSrc()` che sostituiva il path su `window.innerWidth <= 1024`. Sistema immagini gusti semplificato da 4 a 3 varianti per gusto. |
| 2026-03-12 | **B2B Descrizioni minuscole**: aggiunto `text-transform:none` a tutte le descrizioni nelle schede espanse/pannelli dettaglio delle categorie Monoporzioni (`.pezziduri-card__exp-desc`), Torte (`.torte-detail-meta`), Coni (`.coni-detail-meta`), Coppette (`.coppette-detail-meta`), Contenitori (`.contenitori-detail-meta`), Coni Gluten Free (`.conigf-detail-meta`) e Accessori (`.accessori-card__exp-desc`). Le descrizioni ora appaiono in minuscolo, coerenti con la categoria Gusti. |
| 2026-03-11 | **B2B Monoporzioni — nuovi prodotti**: aggiunte 2 nuove schede prodotto nella griglia PEZZI DURI: `Mini Coni` (coni ripieni di Buontalenti®) e `Zuccotto` (zuccotto gelato artigianale). Immagini ottimizzate da PNG a WebP (max 1200px, quality 78). Aggiornate tutte le strutture dati: `PEZZI_DURI_IMAGES`, `CATEGORY_DATA.rows`, `PEZZI_DURI_DESC`, `PEZZI_DURI_DESC_I18N` (EN/FR/ES), `PEZZI_DURI_NAMES_I18N` (IT/EN/FR/ES), tabella listino HTML. |
| 2026-03-11 | **Mercury — pulizia completa**: rimosso `mercury.webp` + tutti i CSS + JS parallax da 5 pagine: `eventi/index.html`, `eventi/evento-esterno/`, `eventi/experience/`, `eventi/saletta-privata-tosinghi/`, `b2b/index.html`. Zero riferimenti residui. |
| 2026-03-11 | **Hub Eventi — outline nere**: corretto `.ev-types__grid` da `gap:2px` a `gap:0` — eliminava sfondo nero visibile come linee tra le card tipologie evento |
| 2026-03-11 | **Homepage CTA**: `.choice-cta` ridisegnato da pill bianco pieno (`align-self:stretch`, `padding:20px 40px`, sfondo bianco solido) a pill frosted-glass compatto (`align-self:flex-start`, `padding:11px 22px`, `backdrop-filter:blur(8px)`, bordo `rgba(255,255,255,0.75)`) |
| 2026-03-11 | **Badiani Dove Vuoi — card redesign**: rimossi sovratitoli (`.ext-card__subtitle`), card quadrate con `aspect-ratio:1/1` e titolo in alto (`align-items:flex-start`), descrizione trasformata in pulsante CTA rosa (stile homepage) con freccia SVG |
| 2026-03-10 | **Homepage**: rimosso testo hero "Badiani Experience" + label "Benvenuti" — video visibile in full-screen |
| 2026-03-10 | **Homepage**: rimossi tutti i sovratitoli (label uppercase) da tutte le sezioni |
| 2026-03-10 | **Homepage**: uniformati tutti i titoli a `clamp(42px, 6vw, 192px)` — stessa misura di IL BUONTALENTI® |
| 2026-03-10 | **Homepage**: rimossa immagine Mercury + CSS + JS parallax correlato |
| 2026-03-10 | **Tipografia**: font-family body aggiornato da `SuperGroteskDigits` a `SuperGroteskC` — numeri e lettere uniformi |
| 2026-03-10 | **Titoli**: rimossa linea grigia decorativa (`.title-accent::after`) — resta solo quadratino rosa |
| 2026-03-10 | **Favicon**: sostituito logo completo con icona "B" — 4 varianti generate (WebP 64px, ICO 32px, PNG 180px, PNG 32px) |
| 2026-03-10 | **Saletta Tosinghi**: aggiunta dicitura "Minimo di spesa applicabile" sotto ogni pacchetto (Silver, Gold, Platinum), localizzata in IT/EN/FR/ES |
| 2026-03-10 | **B2B Gusti grid**: portato a 5 colonne desktop (era 4); mobile 2 colonne (era 3) |
| 2026-03-10 | **B2B Gusti grid — bug fix**: rimosso `grid-auto-flow:dense` che causava spostamento visivo delle card tra categorie al click; rimossa logica DOM-swap difettosa (`.before()` non ripristinava la posizione originale); rimossi override `gridRowStart`/`gridRowEnd` in conflitto con `grid-row:span 2` CSS |
| 2026-03-10 | **B2B Gusti grid — bug fix 2**: rimosso completamente `grid-column:span 2 / grid-row:span 2` dall'expanded card (causa impossibilità di espansione in ultima colonna → salto di riga → gap → incasino categorie); dettaglio gusto ora mostrato nel pannello `#gelatoDetail` sotto la griglia (stessa architettura tipologia vasche) |
| 2026-03-10 | **B2B Gelato card — overlay espansa**: rimosso pannello `#gelatoDetail`; info gusto iniettata come `.gelato-card__exp-body` con `position:absolute; bottom:0` che scorre dal basso sopra la foto |
| 2026-03-10 | **B2B Gelato card — bug fix specificità**: `.gelato-card span` (specificità 0,1,1) sovrastava `.gelato-card__exp-tag` (0,1,0) rendendo i pill allergeni grandi 13px. **Fix**: selettore cambiato in `.gelato-card > span` (solo figlio diretto = etichetta nome); `.gelato-card__exp-tag` protetto con `!important` su tutte le proprietà dimensionali |
| 2026-03-10 | **B2B Categorie**: aggiornati i pulsanti categoria `Gusti`, `Torte`, `Coni & Coppette`, `Contenitori` e `Accessori` con nuovi asset in `assets/images/categories/`; convertite le sorgenti PNG in `gusti.webp`, `torte.webp`, `coni-coppette.webp`, `contenitori.webp`, `accessori.webp` per uso web |

### Debito Tecnico

| # | Area | Descrizione |
|---|------|-------------|
| 3 | **CSS inline** | Ogni pagina ha 200-500 righe di `<style>` inline — difficile manutenzione |
| 4 | **STRINGS duplicati** | Oggetti i18n copiati in 9 file HTML — aggiornamento manuale costoso |
| 5 | **Due sistemi i18n** | `STRINGS` inline + `src/i18n/i18n.js` — approccio incoerente |
| 6 | **CSS non minificato** | `badiani-common.css` non compresso (~30% risparmio potenziale) |
| 7 | **No build pipeline** | Nessun bundling, transpilazione, o ottimizzazione automatica |
| 8 | **Path relativi fragili** | `../assets/gelato/...` si rompe se si sposta il file |
| 9 | **assets/i18n.js orfano** | File non usato, crea confusione |

### Asset Orfani (spazio recuperabile)

- `pdf_extracted/` — ~53 immagini non usate
- `assets/extracted/brochure-italia/` — ~28 pagine non usate
- `foto_torte/` PNG — sostituite da WebP

---

## TODO e Funzionalità Pianificate

### Da fare (dal docs/IMPLEMENTATION-SUMMARY.md)

| Priorità | Task | Stato |
|----------|------|-------|
| 🔴 Alta | Homepage: decidere titolo hero ("Badiani events?" vs "Esperienze Badiani?") | In attesa |
| 🔴 Alta | Homepage: sostituire video con Paolo in laboratorio | In attesa |
| 🟡 Media | Pagina Gelato Van: creare quando pronta | Pianificata |
| 🟡 Media | B2B: aggiornare categorie prodotto da brochure pg. 19 | In attesa |
| 🟡 Media | B2B: aggiungere info allergeni a tutti i prodotti | Parziale |
| 🟡 Media | B2B: galleria foto per tutti i tipi di evento | In attesa |
| 🟡 Media | B2B: showcase loghi clienti | Non iniziata |
| 🟢 Bassa | Testing: responsive mobile/desktop | Non iniziato |
| 🟢 Bassa | Testing: accessibilità WCAG | Non iniziato |
| 🟢 Bassa | Testing: verifica i18n tutte le lingue | Non iniziato |

### Miglioramenti Suggeriti

| Priorità | Miglioramento |
|----------|---------------|
| 🔴 Alta | Centralizzare i18n: sostituire 9 copie STRINGS con JSON + modulo condiviso |
| 🔴 Alta | Estrarre CSS inline in file separati per pagina |
| 🟡 Media | Aggiungere build pipeline (Vite o simile) per minificazione |
| 🟡 Media | Implementare Service Worker per cache offline |
| 🟡 Media | Audit WCAG 2.1 AA completo |
| 🟢 Bassa | Analytics privacy-friendly (Plausible/Fathom) |
| 🟢 Bassa | Dark mode toggle |

---

## Guida per Modifiche Future

### Aggiungere un Nuovo Gusto Gelato

1. **Creare immagini** in `assets/gelato/{NomeGusto}/`:
   - `{gusto}.webp` — immagine principale
   - `{gusto}-2.webp` — immagine dettaglio
2. **Generare thumbnail**: `python scripts/make_gelato_thumbs.py`
3. **Aggiungere oggetto** in `data/gelatoFlavors.js` seguendo la struttura esistente
4. Il gusto apparirà automaticamente nella griglia B2B

### Aggiungere una Nuova Monoporzione (Pezzi Duri)

> ⚠️ **CRITICO**: il renderer `renderPezziDuriGallery` filtra via qualsiasi prodotto che non sia presente **sia** in `CATEGORY_DATA['PEZZI DURI'].rows` **sia** in `PEZZI_DURI_IMAGES`. Se manca uno dei due, la card non appare.

**Tutti i punti sono obbligatori, nell'ordine:**

1. **Ottimizzare l'immagine** PNG/JPG → WebP (max 1200px, quality 72-80), salvare in `assets/images/pezziduri/`:
   ```python
   from PIL import Image
   img = Image.open('prodotto.png')
   img.save('prodotto.webp', 'webp', quality=78)
   ```

2. **`PEZZI_DURI_IMAGES`** (in `b2b/index.html` ~linea 7600) — aggiungere il path immagine:
   ```js
   'Nome Prodotto': '../assets/images/pezziduri/prodotto.webp',
   ```

3. **`CATEGORY_DATA['PEZZI DURI'].rows`** (~linea 6740) — aggiungere la riga dati:
   ```js
   ['Nome Prodotto', '90 g', '24', 'uova, latte, soia'],
   ```
   > ⚠️ Questo è il punto che il renderer usa come sorgente lista prodotti. Se manca qui, la card non viene mai creata, anche se l'immagine è presente.

4. **`PEZZI_DURI_DESC`** (~linea 7222) — descrizione in italiano:
   ```js
   'Nome Prodotto': 'Descrizione in italiano',
   ```

5. **`PEZZI_DURI_DESC_I18N`** (~linea 7237) — descrizione EN, FR, ES (stessa struttura).

6. **`PEZZI_DURI_NAMES_I18N`** (~linea 7287) — nome tradotto in IT (solo se ha `®`), EN, FR, ES.

7. **Tabella listino HTML** (~linea 5060) — aggiungere riga `<tr>` prima di `</tbody>`:
   ```html
   <tr><td class="listino-flavor">Nome Prodotto</td><td class="listino-price">€ X,XX</td><td class="listino-col-center">90 g</td><td class="listino-col-center">24</td></tr>
   ```

**Verifica finale** — controllare che questi 4 grep restituiscano tutti risultati:
```powershell
Select-String -Path "b2b/index.html" -Pattern "Nome Prodotto" | Select-Object LineNumber
```
Devono comparire almeno alle linee di: `CATEGORY_DATA.rows`, `PEZZI_DURI_IMAGES`, `PEZZI_DURI_DESC`, listino `<tr>`.

### Aggiungere una Nuova Pagina

1. Creare `nuova-pagina/index.html`
2. Includere `<link rel="stylesheet" href="../assets/badiani-common.css" />`
3. Copiare struttura topbar + footer da pagina esistente
4. Aggiungere oggetto `STRINGS` con le 4 lingue
5. Aggiornare `sitemap.xml` con il nuovo URL
6. Aggiornare la navigazione nel topbar di tutte le pagine

### Modificare i Testi (i18n)

- **Pagine con STRINGS inline**: Modificare l'oggetto `STRINGS` direttamente nell'HTML
- **Pagina B2B**: Modificare i file JSON in `src/i18n/locales/`
- **Stringhe cookie**: Usare `python _source/add_cookie_strings.py` per aggiornare tutte le pagine

### Aggiungere un Nuovo Evento

1. Creare `eventi/nuovo-evento/index.html`
2. Seguire il pattern di `evento-esterno/` o `saletta-privata-tosinghi/`
3. Aggiornare la griglia in `eventi/index.html`
4. Aggiornare `sitemap.xml`

### Aggiornare il Worker Cloudflare

1. Modificare `cloudflare/contact-api-worker.js`
2. Loggarsi nel Dashboard Cloudflare Workers
3. Incollare il codice aggiornato
4. Testare con form submission reale
5. Verificare ricezione email

### Convenzioni di Commit

```
fix:   correzione bug
feat:  nuova funzionalità
perf:  ottimizzazione performance
chore: manutenzione/pulizia
docs:  aggiornamento documentazione
style: modifiche CSS/visual
i18n:  traduzioni/internazionalizzazione
```

### Regole di Pulizia (da docs/REPO-CLEANUP-NOTES)

1. ✅ Rimuovere originale solo se WebP esiste E nessun codice lo referenzia
2. ✅ Commit separati per tipo (`fix:`, `perf:`, `chore:`)
3. ✅ Evitare refactoring strutturali in un singolo commit
4. ✅ Validare tutte le pagine dopo ogni batch di modifiche

---

## Documentazione Correlata

Per approfondimenti specifici, consultare:

- `docs/IMPLEMENTATION-SUMMARY.md` — Cosa è stato implementato dalla brochure PDF
- `docs/ASSET-AUDIT-REPORT.md` — Inventario completo asset con stato (usato/orfano/rotto)
- `docs/CLOUDFLARE-WORKER-CONTACT-SETUP.md` — Guida passo-passo setup API email
- `docs/content-map-brochure-italia.md` — Mappatura contenuti brochure → pagine sito
- `docs/REPO-CLEANUP-NOTES-2026-02-20.md` — Regole e log pulizia repository

---

*Ultimo aggiornamento: 11 Marzo 2026*
