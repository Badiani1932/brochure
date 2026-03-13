# Catalogo Gelato (Data Layer)

> Allegare questo file quando si lavora su: aggiunta/modifica gusti, dati prodotti, allergeni, immagini gelato.

---

## File: `data/gelatoFlavors.js`

Array di 35 oggetti gusto, esportato come modulo ES6.

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

---

## I 35 Gusti

| # | Gusto | Allergeni chiave | Flag speciali |
| --- | ------- | ----------------- | --------------- |
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

---

## Uso nel B2B

La pagina `b2b/index.html` importa i dati e genera dinamicamente:

- **Griglia gusti**: Cards con immagine + nome + badge allergeni
- **Modali prodotto**: Overlay fullscreen con dettaglio completo (foto, specifiche, allergeni, flag dietetici)
- **Filtri categoria**: 9 categorie (gelato, torte, vasche, pezziduri, coppette, cono, cialde, contenitori, accessori)

---

## Immagini Gusti

Ogni gusto ha 3 varianti immagine:

```text
assets/gelato/{NomeGusto}/
├── {gusto}.webp          # Immagine principale (card)
├── {gusto}-2.webp        # Immagine dettaglio (modale)
└── {gusto}-thumb.webp    # Thumbnail (generata da script)
```

---

## Aggiungere un Nuovo Gusto Gelato

1. **Creare immagini** in `assets/gelato/{NomeGusto}/`:
   - `{gusto}.webp` — immagine principale
   - `{gusto}-2.webp` — immagine dettaglio
2. **Generare thumbnail**: `python scripts/make_gelato_thumbs.py`
3. **Aggiungere oggetto** in `data/gelatoFlavors.js` seguendo la struttura esistente
4. Il gusto apparirà automaticamente nella griglia B2B

---

## Aggiungere una Nuova Monoporzione (Pezzi Duri)

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
