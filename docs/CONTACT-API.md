# Form di Contatto e API

> Allegare questo file quando si lavora su: form contatto, Cloudflare Worker, invio email, troubleshooting API.

---

## Architettura

```text
[Browser Form] --POST JSON--> [Cloudflare Worker] --OAuth2--> [Gmail API] --> Email
```

---

## Frontend (Form HTML)

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

---

## Backend — `cloudflare/contact-api-worker.js`

| Endpoint | Metodo | Descrizione |
| ---------- | -------- | ------------- |
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

---

## Configurazione Worker (`wrangler.toml`)

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

---

## Troubleshooting Form

| Errore | Causa | Fix |
| -------- | ------- | ----- |
| 403 | Origin non nella whitelist | Aggiornare `ALLOWED_ORIGIN` in wrangler.toml |
| 502 | Credenziali OAuth scadute/errate | Rinnovare `GOOGLE_REFRESH_TOKEN` nel dashboard |
| 404 | Path errato | Verificare endpoint `/send` |
| 500 | Config mancante | Verificare variabili env nel Worker |

---

## Aggiornare il Worker Cloudflare

1. Modificare `cloudflare/contact-api-worker.js`
2. Loggarsi nel Dashboard Cloudflare Workers
3. Incollare il codice aggiornato
4. Testare con form submission reale
5. Verificare ricezione email
