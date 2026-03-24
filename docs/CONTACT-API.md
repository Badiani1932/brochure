# Form di Contatto

> Allegare questo file quando si lavora su: form contatto, invio email, troubleshooting.

---

## Architettura

```text
[Browser Form] --AJAX POST--> [FormSubmit.co] --> Email a eventi@badiani1932.com
```

Zero backend. Le form HTML inviano direttamente a FormSubmit.co via AJAX.

---

## Frontend (Form HTML)

Presente in: `/index.html`, `/b2b/index.html`, `/eventi/index.html`, `/eventi/evento-esterno/index.html`, `/eventi/saletta-privata-tosinghi/index.html`, `/eventi/experience/index.html`

```javascript
// Endpoint (uguale in tutte le pagine)
var CONTACT_API_ENDPOINT = 'https://formsubmit.co/ajax/eventi@badiani1932.com';

// Payload inviato a FormSubmit
{
  name: "Nome Cognome",
  email: "cliente@email.com",
  message: "=== RICHIESTA ===\n...",  // Corpo testuale formattato
  _subject: "Richiesta Informazioni - Nome Cognome",
  _replyto: "cliente@email.com",
  _captcha: "false"
}
```

Ogni form costruisce il `message` come testo formattato con tutti i campi del modulo.

---

## Provider — [FormSubmit.co](https://formsubmit.co)

- **Gratis**, illimitato, zero backend
- AJAX via `https://formsubmit.co/ajax/<email>`
- Risposta: `{"success":"true"}` oppure `{"success":"false","message":"..."}`
- Prima attivazione: email di conferma una tantum al destinatario

**Nessun worker Cloudflare necessario.** Il file `cloudflare/contact-api-worker.js` è legacy.

---

## Troubleshooting Form

| Errore | Causa | Fix |
| -------- | ------- | ----- |
| `success: false` + "needs activation" | Form non ancora attivata | Controllare email di eventi@ e cliccare "Activate Form" |
| `success: false` + altro messaggio | Errore FormSubmit | Verificare formato payload |
| CORS error | Browser blocca la richiesta | FormSubmit gestisce CORS automaticamente |
| Form non invia | JS error | Controllare console browser |

---

## Cambiare email destinatario

Se serve cambiare da `eventi@badiani1932.com` a un'altra email:

1. Cercare `formsubmit.co/ajax/eventi@badiani1932.com` in tutti i file HTML
2. Sostituire con il nuovo indirizzo
3. Inviare un form di test — FormSubmit invierà email di attivazione al nuovo indirizzo
4. Cliccare "Activate Form" nell'email
