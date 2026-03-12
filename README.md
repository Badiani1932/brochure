# Badiani 1932 — Brochure Digitale (Eventi & B2B)

> Sito web brochure premium per **Badiani 1932**, storica gelateria artigianale fiorentina.
> Il sito serve come piattaforma B2B e per eventi aziendali — non è un e-commerce né un sito consumer.

**Live URL**: `https://www.badiani1932.com/`
**Repository**: `Badiani1932/badianibroshure` (branch: `main`)

> **Regola operativa**: Tutte le immagini fornite devono essere **ottimizzate per il web** prima di essere inserite nel sito.

---

## Stack Tecnologico

| Livello | Tecnologia |
| --------- | ----------- |
| **Frontend** | HTML5, CSS3, JavaScript vanilla (nessun framework) |
| **CSS** | Custom Properties + `clamp()` + Grid/Flexbox |
| **Font** | SuperGrotesk (4 varianti custom `@font-face`) |
| **Immagini** | WebP (primario) + PNG/JPG fallback |
| **Dati** | JS statico (`gelatoFlavors.js`) — nessun CMS/DB |
| **i18n** | 4 lingue (IT, EN, FR, ES) |
| **API** | Cloudflare Worker (serverless) per email |
| **Hosting** | Sito statico + Worker Cloudflare |

Il sito è **completamente autocontenuto** — nessuna dipendenza esterna CDN, nessun npm.

---

## Mappa delle Pagine

| Pagina | File | Funzione |
| -------- | ------ | ---------- |
| **Homepage** | `index.html` | Landing page, storia, video hero |
| **Hub Eventi** | `eventi/index.html` | Catalogo tipologie evento |
| **Saletta Privata** | `eventi/saletta-privata-tosinghi/` | Pacchetti Silver / Gold / Platinum |
| **Evento Esterno** | `eventi/evento-esterno/` | Cool Box / Carretto / Vetrina |
| **Speciale Aziende** | `eventi/speciale-aziende/` | Eventi corporate personalizzati |
| **Experience** | `eventi/experience/` | Esperienza Badiani |
| **Catalogo B2B** | `b2b/index.html` | Prodotti, gusti, formati, allergeni |
| **Magazine** | `magazine/index.html` | Rassegna stampa |
| **Cookie Policy** | `cookie-policy.html` | Policy cookie GDPR |
| **Privacy** | `privacy.html` | Informativa privacy GDPR |

---

## Documentazione per Categoria

La documentazione tecnica è suddivisa in file tematici nella cartella `docs/`.
**Allega solo il file pertinente** quando lavori su una specifica area del sito.

| File | Contenuto | Quando allegare |
| ------ | ----------- | ----------------- |
| [`ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Design system, CSS, componenti, animazioni, responsive, a11y | Modifiche CSS, layout, componenti |
| [`I18N.md`](docs/I18N.md) | Sistema i18n, 4 lingue, STRINGS, persistenza | Traduzioni, aggiunta lingue/testi |
| [`GELATO-CATALOG.md`](docs/GELATO-CATALOG.md) | Data layer gelato, 27 gusti, allergeni, guide aggiunta gusti | Catalogo B2B, nuovi gusti, monoporzioni |
| [`ASSETS.md`](docs/ASSETS.md) | Immagini, ottimizzazione, favicon, script | Gestione asset, immagini, ottimizzazione |
| [`CONTACT-API.md`](docs/CONTACT-API.md) | Form contatto, Cloudflare Worker, email API | Form, invio email, troubleshooting API |
| [`SEO-LEGAL.md`](docs/SEO-LEGAL.md) | SEO, meta tag, sitemap, GDPR, cookie, privacy | SEO, indicizzazione, conformità legale |
| [`GUIDES.md`](docs/GUIDES.md) | Guide operative, script, convenzioni commit | Aggiunta pagine, eventi, manutenzione |
| [`TECH-DEBT.md`](docs/TECH-DEBT.md) | Problemi noti, TODO, changelog, debito tecnico | Pianificazione, manutenzione, stato progetto |

---

## Struttura del Repository

```text
badianibroshure/
+-- index.html                      # Homepage
+-- cookie-policy.html              # Cookie (GDPR)
+-- privacy.html                    # Privacy (GDPR)
+-- robots.txt / sitemap.xml        # SEO
+-- assets/
|   +-- badiani-common.css          # Stile condiviso
|   +-- fonts/                      # SuperGrotesk
|   +-- gelato/                     # 27 cartelle gusto (3 img ciascuna)
|   +-- images/                     # Foto per categoria
|   +-- video/                      # Video hero
+-- data/gelatoFlavors.js           # Dati catalogo gelato
+-- src/i18n/i18n.js                # Modulo i18n ES6 (B2B)
+-- b2b/index.html                  # Catalogo B2B
+-- eventi/                         # Pagine eventi (hub + sottopagine)
+-- magazine/index.html             # Rassegna stampa
+-- cloudflare/                     # Worker API contatto
+-- scripts/                        # Script Python di utility
+-- _source/                        # Script sorgente
+-- docs/                           # Documentazione tecnica
```
