# Guide Operative

> Allegare questo file quando si deve: aggiungere pagine, eventi, aggiornare il worker, o seguire convenzioni di progetto.

---

## Aggiungere una Nuova Pagina

1. Creare `nuova-pagina/index.html`
2. Includere `<link rel="stylesheet" href="../assets/badiani-common.css" />`
3. Copiare struttura topbar + footer da pagina esistente
4. Aggiungere oggetto `STRINGS` con le 4 lingue
5. Aggiornare `sitemap.xml` con il nuovo URL
6. Aggiornare la navigazione nel topbar di tutte le pagine

---

## Aggiungere un Nuovo Evento

1. Creare `eventi/nuovo-evento/index.html`
2. Seguire il pattern di `evento-esterno/` o `saletta-privata-tosinghi/`
3. Aggiornare la griglia in `eventi/index.html`
4. Aggiornare `sitemap.xml`

---

## Script di Utilità

### Python Scripts (`scripts/`)

| Script | Scopo | Input | Output |
| -------- | ------- | ------- | -------- |
| `make_gelato_thumbs.py` | Genera thumbnail 420px per gusti gelato | `assets/gelato/*/` | `*-thumb.webp` (quality 80) |
| `optimize_b2b_modal_images.py` | Converti PNG/JPG → WebP ottimizzato | Cartelle prodotti | WebP (hero: 1800px, default: 1200px, quality 72) |
| `optimize_detail_images.py` | Ottimizza immagini dettaglio | Cartelle specifiche | WebP ottimizzato |
| `extract_docx_links.py` | Estrae hyperlink da DOCX → JSON | File .docx | JSON con titolo + URL |
| `extract_docx_tables.py` | Estrae tabelle da DOCX | File .docx | Dati strutturati |
| `fix-encoding.ps1` | Fix encoding caratteri | File con encoding errato | File corretti |

### Source Scripts (`_source/`)

| Script | Scopo | Note |
| -------- | ------- | ------ |
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

## Convenzioni di Commit

```text
fix:   correzione bug
feat:  nuova funzionalità
perf:  ottimizzazione performance
chore: manutenzione/pulizia
docs:  aggiornamento documentazione
style: modifiche CSS/visual
i18n:  traduzioni/internazionalizzazione
```

---

## Regole di Pulizia (da docs/REPO-CLEANUP-NOTES)

1. ✅ Rimuovere originale solo se WebP esiste E nessun codice lo referenzia
2. ✅ Commit separati per tipo (`fix:`, `perf:`, `chore:`)
3. ✅ Evitare refactoring strutturali in un singolo commit
4. ✅ Validare tutte le pagine dopo ogni batch di modifiche

---

## Troubleshooting Rapido VS Code

> **Prima di investigare qualsiasi anomalia visiva o di file in VS Code, prova queste soluzioni in ordine:**

| # | Sintomo | Soluzione immediata |
| --- | --------- | --------------------- |
| 1 | Pagina appare con design vecchio/diverso nell'anteprima | **Riavvia VS Code** — la preview può rimanere in cache con versione obsoleta |
| 2 | File modificato ma le modifiche non sembrano applicate | Riavvia VS Code oppure `Developer: Reload Window` (Ctrl+Shift+P) |
| 3 | Git diff mostra caratteri strani (es. `┬«` invece di `®`) | Falso allarme — è solo il terminale PowerShell che non renderizza UTF-8; il file è corretto |
| 4 | Errori lint in file non toccati | Cache linter stantia — riavvia VS Code |
| 5 | Estensione non risponde o tool fallisce | Riavvia VS Code |

**Regola d'oro**: Se qualcosa sembra rotto ma git conferma che il file è identico a HEAD e il sito live funziona → **riavvia VS Code prima di fare qualsiasi modifica**.
