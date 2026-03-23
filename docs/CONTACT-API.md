# Form di Contatto e API

> Allegare questo file quando si lavora su: form contatto, Cloudflare Worker, invio email, troubleshooting API.

---

## Architettura

```text
[Browser Form] --POST JSON--> [Cloudflare Worker] --API Key--> [Resend API] --> Email
```

---

## Frontend (Form HTML)

Presente in: `/eventi/index.html`, `/b2b/index.html`, `/index.html`, `/eventi/evento-esterno/index.html`, `/eventi/saletta-privata-tosinghi/index.html`

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

**Email provider**: [Resend](https://resend.com) — singola chiamata POST a `https://api.resend.com/emails`.

**Classificazione automatica** dei messaggi:

- Source/fields "b2b", azienda, partitaIva → tag `[B2B]`
- Source/fields "event", tosinghi, esterno → tag `[EVENTI]`
- Default → tag `[WEB]`

**Sicurezza**:

- Validazione origin (whitelist in env vars)
- Sanitizzazione subject (max 200 char, single-line)
- Pulizia body messaggio
- No dettagli interni negli errori al client
- Request ID per tracciamento

---

## Configurazione Worker (`wrangler.toml`)

```toml
name = "badianiapiwebmail"
[vars]
ALLOWED_ORIGIN = "https://www.badiani1932.com,https://badiani1932.github.io"
MAIL_TO = "eventi@badiani1932.com"
MAIL_FROM = "noreply@badiani1932.com"
```

**Secret** (impostati via `npx wrangler secret put`, mai nel codice):

- `RESEND_API_KEY`

**Requisiti dominio**: il dominio `badiani1932.com` deve essere verificato su Resend con record DNS (SPF, DKIM, CNAME).

---

## Troubleshooting Form

| Errore | Causa | Fix |
| -------- | ------- | ----- |
| 403 | Origin non nella whitelist | Aggiornare `ALLOWED_ORIGIN` in wrangler.toml |
| 502 | API key Resend errata o dominio non verificato | Verificare `RESEND_API_KEY` e DNS su resend.com |
| 404 | Path errato | Verificare endpoint `/send` |
| 500 | Config mancante | Verificare variabili env nel Worker |

---

## Aggiornare il Worker Cloudflare

1. Modificare `cloudflare/contact-api-worker.js`
2. Eseguire `cd cloudflare && npx wrangler deploy`
3. Testare con form submission reale
4. Verificare ricezione email
