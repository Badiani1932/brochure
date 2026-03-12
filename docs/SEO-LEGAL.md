# SEO, Indicizzazione e Conformità Legale

> Allegare questo file quando si lavora su: meta tag, SEO, sitemap, robots.txt, cookie policy, privacy, GDPR.

---

## Meta Tags (ogni pagina)

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

---

## Dati Strutturati

- **Schema.org BreadcrumbList** sulla homepage
- `<meta name="theme-color" content="#1e398d">`

---

## Sitemap (`sitemap.xml`)

7 pagine principali indicizzate + privacy e cookie policy.
Frequenza: mensile (pagine statiche), settimanale (magazine).

---

## Robots.txt

```text
Allow: /                  # Tutto il contenuto pubblico
Disallow: /_source/       # Script sorgente
Disallow: /scripts/       # Script utility
Disallow: /docs/          # Documentazione interna
Disallow: /assets/docs/   # Documenti PDF
```

---

## Content Security Policy (CSP)

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
