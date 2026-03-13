# Problemi Noti, Debito Tecnico e TODO

> Allegare questo file quando si pianifica lavoro, si fa manutenzione, o si vuole sapere lo stato del progetto.

---

## Problemi Critici

| # | Problema | Impatto | Fix Suggerito |
| --- | --------- | --------- | --------------- |
| 1 | File `.woff2` mancanti per SuperGroteskB/A | Font ~20% più pesanti (solo .woff caricati) | Verificare e copiare .woff2 se disponibili |
| 2 | Preload `.woff2` nel HTML ma file non esistono | Browser tenta download 404, poi fallback a .woff | Rimuovere preload `.woff2` dal `<head>` o procurare i file |

---

## Modifiche Recenti (Mar 2026)

| Data | Modifica |
| ------ | ---------- |
| 2026-03-14 | **Topbar fissa — fix scroll**: cambiato `position:sticky` → `position:fixed` su `.topbar` (sticky era rotto da `html{overflow-x:hidden}` che creava un nuovo scroll container). Aggiunta `--topbar-h: calc(36px + clamp(42px,4vw,55px))` in `:root` con override `68px`@768px / `60px`@400px. `body{padding-top:var(--topbar-h)}` compensa il layout; `html{scroll-padding-top:var(--topbar-h)}` allinea i link anchor. Rimosso `overflow-x:hidden` da `html` (tenuto solo `clip`). `.topbar__mobile-nav` ora usa `top:var(--topbar-h)` e `max-height:calc(100vh - var(--topbar-h))`. |
| 2026-03-14 | **Desktop lang — dropdown custom**: sostituito `<select>` nativo con dropdown completamente custom (`.topbar__lang-dd`). La finestrella nativa del browser (non stilabile) è rimpiazzata da un pannello Badiani-blue arrotondato con 4 `.topbar__lang-opt` — stile identico ai bottoni del pannello mobile (uppercase, letter-spacing 1.5px, hover rosa). Il `<select id="langSelect">` rimane nel DOM con attributo `hidden` come sorgente di verità per il sistema i18n; i bottoni dispatchano `change` su di esso. Trigger `.topbar__lang-trigger` styled come nav link (pill, hover rosa). Chiusura su click esterno. IIFE aggiunta su tutti e 10 i file HTML + `badiani-common.css`. |
| 2026-03-14 | **Mobile nav lingua — bottoni stile nav**: sostituito `<select>` nel pannello hamburger con 4 `<button class="topbar__mobile-lang-btn">` in riga flex. Stile identico alle voci nav (uppercase, letter-spacing 1.5px, hover rosa `var(--badiani-pink)`). Lingua attiva evidenziata con classe `.is-active`. JS IIFE aggiornato: i bottoni settano direttamente `.value` sul `<select>` desktop e dispatchano `change`; `.is-active` sincronizzata anche su cambio lingua da desktop. Applicato su tutti e 10 i file HTML + `assets/badiani-common.css`. |
| 2026-03-14 | **Mobile nav — pannello compatto**: sostituito overlay fullscreen con pannello laterale destro (`width:260px; right:0; border-radius:0 0 0 10px`). Accordion `<details>/<summary>` rimpiazzato da `<div class="topbar__mobile-group">` con `<a>` navigabile alla pagina principale della sezione + `<button class="topbar__mobile-group-toggle">` separato per espandere i sotto-link. JS accordion aggiunto su tutti e 10 i file HTML. Modifiche applicate a: `index.html`, `magazine/`, `b2b/`, `eventi/index.html`, `eventi/evento-esterno/`, `eventi/experience/`, `eventi/saletta-privata-tosinghi/`, `eventi/speciale-aziende/`, `cookie-policy.html`, `privacy.html`. |
| 2026-03-13 | **SEO audit completo — implementazione professionale**: eseguito audit SEO su tutti e 10 i file HTML con script `scripts/seo_analyzer.py` (analizza title/desc/H1/OG/Twitter Card/hreflang/Schema.org/alt/robots/favicon/encoding/heading hierarchy). Score iniziale: 8 critici + 27 avvertenze → finale: 0 critici + 3 avvertenze. Interventi: (1) **Encoding Mojibake** — creato `scripts/fix_encoding.py`, 526 sostituzioni su 4 file (cookie-policy.html, privacy.html, evento-esterno, saletta-privata-tosinghi) — tutti i caratteri accentati/speciali corretti inclusi sequenze W1252 high-byte (0x80–0x9F). (2) **Schema.org homepage** — rimpiazzato singolo `Organization` con array JSON-LD: `WebSite` + `Organization`/`LocalBusiness`/`IceCreamShop` (legalName: "Sviluppo Gelato S.r.l.") + `BreadcrumbList`. (3) **OG image** — aggiunti `og:image:width: 1665`, `og:image:height: 643`, `og:image:type: image/webp` su tutti e 10 i file. (4) **Meta robots** — aggiunto tag robots a tutte le pagine (`index,follow` + max-snippet/max-image-preview per le pagine principali; `noindex,follow` per cookie-policy e privacy). (5) **Preconnect** — aggiunto `preconnect` + `dns-prefetch` per l'endpoint Cloudflare Worker su tutte le pagine. (6) **H1 B2B** — "B2B" → "Gelato Artigianale B2B" (IT), "Artisan Gelato B2B" (EN/FR/ES) nelle 4 stringhe STRINGS. (7) **sitemap.xml** — namespace `xmlns:xhtml`, `lastmod` aggiornate a 2026-03-13, priorità sott-pagine eventi 0.7→0.8, pagine legali 0.3→0.2. (8) **robots.txt** — aggiunti `Disallow: /cloudflare/`, `/data/`, `/*?`. (9) **Accessibility** — `aria-hidden="true"` su 6 immagini placeholder JS-driven in b2b/, eventi/, evento-esterno/, saletta-privata-tosinghi/. |
| 2026-03-13 | **B2B Modale — scrollbar nascoste**: aggiunta regola globale `scrollbar-width:none` + `::-webkit-scrollbar{display:none}` su `.modal__content` e tutti i figli (`*`). Nessuna barra di scorrimento visibile in nessuna sezione del modale B2B, scroll comunque funzionante. |
| 2026-03-13 | **B2B Monoporzioni — vetrina full-bleed scrollabile**: hero overlay `.pezziduri-hero-overlay` ridisegnato da card con bordi arrotondati + ombra a immagine full-bleed edge-to-edge. Rimossi `border-radius`, `box-shadow`, `margin`. Margini negativi per annullare il padding di `.modal__content`. Immagine con `object-fit:contain` e `height:auto` — scrollabile verticalmente su desktop e mobile. Stato overlay con `padding:0` e `overflow-y:auto`. |
| 2026-03-13 | **Gelato — rimosse varianti mobile light**: eliminato il sistema di immagini `-2-light.webp` per mobile (27 file, ~1 MB). Tutti i dispositivi ora caricano la stessa immagine dettaglio `-2.webp`. Rimossa la funzione `getDetailImageSrc()` che sostituiva il path su `window.innerWidth <= 1024`. Sistema immagini gusti semplificato da 4 a 3 varianti per gusto. |
| 2026-03-12 | **Homepage — fix BOM**: rimosso UTF-8 BOM (`EF BB BF`) re-introdotto nel commit precedente prima di `<!DOCTYPE html>`. Corretto preload stale (`vasche.webp` → `b2b-hero.webp`) per allineamento con l'immagine effettiva della choice card B2B. |
| 2026-03-12 | **B2B Tipologia cards — allineamento ai gusti**: convertite le card "Formato Acquisto" allo stesso pattern visivo e interattivo delle card gelato. CSS: bordo, radius, ombra, hover, font identici. Responsive: 5→4@1200→3@1024→2@768 colonne. Espansione in-card con overlay `.tipologia-card__exp-body` (replace del vecchio pannello esterno `.tipologia-detail-panel`). Aggiunto pulsante zoom `.card-zoom` con SVG expand icon. |
| 2026-03-12 | **B2B Coni Gluten Free — fix layout dettaglio**: centrato testo nel pannello dettaglio (`.conigf-detail-info`, `.conigf-detail-name`, `.conigf-detail-meta`). Rimossi override mobile che rimpicciolivano il font. Aggiunto `text-transform:uppercase` sui label. |
| 2026-03-12 | **Eventi Modali — pulsante zoom**: aggiunto pulsante expand (`.modal-hero__zoom`) in alto a destra sulle foto di Cool Box e Carretto nei modali di `evento-esterno/`. Immagini wrappate in `.modal-hero__img-wrap` con `position:relative`. Stile identico al `.card-zoom` di B2B. Click apre il lightbox esistente (`.img-lightbox`) con gallery per Cool Box. |
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

---

## Debito Tecnico

| # | Area | Descrizione |
| --- | ------ | ------------- |
| 3 | **CSS inline** | Ogni pagina ha 200-500 righe di `<style>` inline — difficile manutenzione |
| 4 | **STRINGS duplicati** | Oggetti i18n copiati in 9 file HTML — aggiornamento manuale costoso |
| 5 | **Due sistemi i18n** | `STRINGS` inline + `src/i18n/i18n.js` — approccio incoerente |
| 6 | **CSS non minificato** | `badiani-common.css` non compresso (~30% risparmio potenziale) |
| 7 | **No build pipeline** | Nessun bundling, transpilazione, o ottimizzazione automatica |
| 8 | **Path relativi fragili** | `../assets/gelato/...` si rompe se si sposta il file |
| 9 | **assets/i18n.js orfano** | File non usato, crea confusione |

### Asset Orfani

- `assets/i18n.js` — file orfano, non importato da nessuna pagina (può essere eliminato)

---

## TODO e Funzionalità Pianificate

### Da fare

| Priorità | Task | Stato |
| ---------- | ------ | ------- |
| 🔴 Alta | Homepage: decidere titolo hero ("Badiani events?" vs "Esperienze Badiani?") | In attesa |
| 🔴 Alta | Homepage: sostituire video con Paolo in laboratorio | In attesa |
| 🟡 Media | Pagina Gelato Van: creare quando pronta | Pianificata |
| 🟡 Media | B2B: aggiornare categorie prodotto da brochure pg. 19 | In attesa |
| 🟡 Media | B2B: aggiungere info allergeni a tutti i prodotti | Parziale |
| 🟡 Media | B2B: galleria foto per tutti i tipi di evento | In attesa |
| 🟡 Media | B2B: showcase loghi clienti (Crystal Cruises, Frescobaldi, Gilli, Paszkowski, Carlton Beach Club, Tiratissima, Bagno Onda, La Versiliana, Cibreo) | Non iniziata |
| 🟡 Media | B2B: creare email dedicata B2B (attualmente solo eventi@) | Non iniziata |
| 🟡 Media | B2B: peso torte SMALL e MEDIUM da aggiungere | Non iniziata |
| 🟢 Bassa | Testing: responsive mobile/desktop | Non iniziato |
| 🟢 Bassa | Testing: accessibilità WCAG | Non iniziato |
| 🟢 Bassa | Testing: verifica i18n tutte le lingue | Non iniziato |

### Miglioramenti Suggeriti

| Priorità | Miglioramento |
| ---------- | --------------- |
| 🔴 Alta | Centralizzare i18n: sostituire 9 copie STRINGS con JSON + modulo condiviso |
| 🔴 Alta | Estrarre CSS inline in file separati per pagina |
| 🟡 Media | Aggiungere build pipeline (Vite o simile) per minificazione |
| 🟡 Media | Implementare Service Worker per cache offline |
| 🟡 Media | Audit WCAG 2.1 AA completo |
| 🟢 Bassa | Analytics privacy-friendly (Plausible/Fathom) |
| 🟢 Bassa | Dark mode toggle |

---

## Documentazione Correlata

Vedi [README.md](../README.md) per l'indice completo della documentazione per categoria.
