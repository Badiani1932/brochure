# Architettura del Design

> Allegare questo file quando si lavora su: CSS, layout, componenti UI, animazioni, responsive design.

---

## Design System

Il sito usa un design system coerente basato su:

### Palette Colori (CSS Custom Properties)

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

### Spacing Scale

```css
:root {
  --space-xxl: 90px;    /* Sezioni principali */
  --space-xl:  72px;    /* Padding hero/sezioni */
  --space-lg:  48px;    /* Gap tra elementi */
  --space-md:  28px;    /* Padding interni */
}
```

### Tipografia

| Font | Uso | File |
| ------ | ----- | ------ |
| **SuperGroteskB** (Condensed Medium) | Titoli `h1, h2, h3`, hero text | `SuperGroteskB-CdMed.woff` |
| **SuperGroteskA** (Regular) | Testo corpo, paragrafi | `SuperGroteskA-Rg[7511].woff` |
| **SuperGroteskDigits** | Solo numeri 0-9 (unicode-range: U+0030-0039) | `SuperGroteskC-MedLF.otf` |
| **SuperGroteskC** (Full) | Elementi specifici che lo referenziano | `SuperGroteskC-MedLF.otf` |

- Titoli: `font-family: 'SuperGroteskDigits', 'SuperGroteskB', 'SuperGroteskA', sans-serif`
- Corpo: `font-family: 'SuperGroteskDigits', 'SuperGroteskA', 'SuperGroteskB', sans-serif`
- Tipografia fluida con `clamp()`: es. `font-size: clamp(28px, 3.6vw, 48px)`

### Decorazione Titoli — `.title-accent`

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

---

## Componenti Condivisi (in `badiani-common.css`)

| Componente | Classe | Descrizione |
| ----------- | -------- | ------------- |
| **Topbar** | `.topbar` | Header sticky blu, logo + nav + selettore lingua + hamburger mobile |
| **Mobile Nav** | `.topbar__mobile-nav` | Overlay fullscreen con animazione slide-in |
| **Hamburger** | `.topbar__hamburger` | Icona animata ☰ ↔ ✕ |
| **Selettore Lingua** | `.topbar__select` | Dropdown custom con chevron SVG inline |
| **Footer** | `.site-footer` | Grid 4 colonne (brand, navigazione, servizi, legale) |
| **Cookie Banner** | `.cookie-banner` | Banner sticky bottom con accept + info |
| **Skip Link** | `.skip-link` | Link accessibilità (visibile solo su focus) |
| **Title Accent** | `.title-accent` | Decorazione quadrato rosa sui titoli |

---

## Pattern di Animazione

| Pattern | Proprietà | Durata |
| --------- | ---------- | -------- |
| **Page Reveal** | `opacity: 0 → 1` + `translateY(-16px → 0)` | 0.6s + stagger 0.04s-0.88s |
| **Card Hover** | `scale(1.06)` + brightness ridotta | 0.3s-0.8s `cubic-bezier(0.4, 0, 0.2, 1)` |
| **Nav Hover** | `translateY(-2px)` + sfondo rosa | 0.3s |
| **Modal Open** | `opacity: 0 → 1` + backdrop blur | 0.3s |
| **Reduced Motion** | Tutte le animazioni disabilitate | `@media (prefers-reduced-motion: reduce)` |

### Pulsante Zoom / Espandi Immagine

Pattern riutilizzabile per espandere immagini a tutto schermo. Cerchio semitrasparente con blur, icona expand SVG bianca, hover scale.

| Pagina | Classe | Contenitore |
| ------- | -------- | ------------- |
| B2B Gusti | `.gelato-card__zoom` | `.gelato-card__media` |
| B2B Tipologia/Pezzi Duri/Accessori | `.card-zoom` | `.tipologia-media`, `.pezziduri-media` |
| B2B Pezzi Duri Lingotto | `.card-zoom--plating` | `.pezziduri-media` (variante rosa con gradiente) |
| Eventi Modali (Cool Box, Carretto) | `.modal-hero__zoom` | `.modal-hero__img-wrap` |

```css
/* Pattern base (B2B) */
.card-zoom {
  position:absolute; top:10px; right:10px;
  width:52px; height:52px; border-radius:999px;
  border:1.5px solid rgba(255,255,255,0.7);
  background:rgba(0,0,0,0.35); backdrop-filter:blur(8px);
  z-index:5;
}
/* SVG icona expand */
<polyline points="15 3 21 3 21 9" />
<polyline points="9 21 3 21 3 15" />
<line x1="21" y1="3" x2="14" y2="10" />
<line x1="3" y1="21" x2="10" y2="14" />
```

- **B2B**: click apre `openFullscreenImage()` (overlay `.fullscreen-overlay` con nav prev/next e dots)
- **Eventi**: click apre `openLightbox()` (overlay `.img-lightbox` con gallery per Cool Box)

### Category Cards (B2B)

Le category card nella pagina B2B usano lo stesso pattern visivo delle choice card della homepage:

- **Titoli in alto a sinistra** (`.category-title` dentro `.category-card__overlay` con `justify-content:flex-start`)
- **Descrizioni come CTA button** (`.category-cta` con freccia SVG, sfondo `--badiani-blue`, hover bianco)
- Al passaggio del mouse il bottone diventa bianco con testo blu e la freccia scorre a destra

---

## Pattern CSS Ricorrenti

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

## Responsive Design e Breakpoint

### Breakpoint

| Breakpoint | Target | Effetto Principale |
| ----------- | -------- | ------------------- |
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

## Accessibilità (a11y)

### Implementato

| Feature | Dettaglio |
| --------- | ---------- |
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
