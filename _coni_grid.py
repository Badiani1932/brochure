"""Rewrite Coni/Coppette section from hero-map layout to pezziduri-style card grid.
   Uses DOM patching for expand/collapse (no flash), zoom with gallery slides.
"""
import pathlib, re, json

fp = pathlib.Path(r'b2b/index.html')
src = fp.read_text(encoding='utf-8')
orig_len = len(src)

# ──────────────────────────────────────────────────────────────
# 1. Update CONI_COPPETTE_IMAGES to use new optimized individual WebPs
# ──────────────────────────────────────────────────────────────
old_images = """      const CONI_COPPETTE_IMAGES = {
        'PICCOLO':          '../assets/images/coni-coppette/sottozero.webp',
        'MEDIO':            '../assets/images/coni-coppette/maxi1.webp',
        'GRANDE':           '../assets/images/coni-coppette/maxi2.webp',
        'Piccola':  '../assets/images/coni-coppette/Bicchierini 16B.webp',
        'Media':    '../assets/images/coni-coppette/Bicchierini 108.webp',
        'Grande':   '../assets/images/coni-coppette/Bicchierini 4C.webp',
        'Maxi':     '../assets/images/coni-coppette/Bicchierini 4CA.webp'
      };"""

new_images = """      const CONI_COPPETTE_IMAGES = {
        'PICCOLO':  '../assets/images/coni-coppette/piccolo.webp',
        'MEDIO':    '../assets/images/coni-coppette/medio.webp',
        'GRANDE':   '../assets/images/coni-coppette/grande.webp',
        'Piccola':  '../assets/images/coni-coppette/Bicchierini 16B.webp',
        'Media':    '../assets/images/coni-coppette/Bicchierini 108.webp',
        'Grande':   '../assets/images/coni-coppette/Bicchierini 4C.webp',
        'Maxi':     '../assets/images/coni-coppette/Bicchierini 4CA.webp'
      };

      const CONI_COPPETTE_ZOOM_IMAGES = {
        'PICCOLO':  '../assets/images/coni-coppette/sottozero.webp',
        'MEDIO':    '../assets/images/coni-coppette/maxi1.webp',
        'GRANDE':   '../assets/images/coni-coppette/maxi2.webp',
        'Piccola':  '../assets/images/coni-coppette/GROUP COPPETTE.webp',
        'Media':    '../assets/images/coni-coppette/GROUP COPPETTE.webp',
        'Grande':   '../assets/images/coni-coppette/GROUP COPPETTE.webp',
        'Maxi':     '../assets/images/coni-coppette/GROUP COPPETTE.webp'
      };"""

assert old_images in src, "CONI_COPPETTE_IMAGES not found"
src = src.replace(old_images, new_images, 1)
print("1. Updated CONI_COPPETTE_IMAGES + added CONI_COPPETTE_ZOOM_IMAGES")

# ──────────────────────────────────────────────────────────────
# 2. Update CONIGF_IMAGES to use new optimized WebPs
# ──────────────────────────────────────────────────────────────
old_gf_images = """      const CONIGF_IMAGES = {
        'Coni Gluten free (083)': '../assets/images/coni-coppette/glutenfree piccolo.webp',
        'Coni Gluten free (084)': '../assets/images/coni-coppette/glutenfreemedio.webp'
      };"""

new_gf_images = """      const CONIGF_IMAGES = {
        'Coni Gluten free (083)': '../assets/images/coni-coppette/gf_piccolo.webp',
        'Coni Gluten free (084)': '../assets/images/coni-coppette/gf_medio.webp'
      };

      const CONIGF_ZOOM_IMAGES = {
        'Coni Gluten free (083)': '../assets/images/coni-coppette/glutenfree piccolo.webp',
        'Coni Gluten free (084)': '../assets/images/coni-coppette/glutenfreemedio.webp'
      };"""

assert old_gf_images in src, "CONIGF_IMAGES not found"
src = src.replace(old_gf_images, new_gf_images, 1)
print("2. Updated CONIGF_IMAGES + added CONIGF_ZOOM_IMAGES")

# ──────────────────────────────────────────────────────────────
# 3. Replace renderConiCoppetteGallery with card-grid version
# ──────────────────────────────────────────────────────────────
render_start = "      function renderConiCoppetteGallery(rows){"
render_end_marker = "      function setupCoppetteInteraction(){"
i1 = src.index(render_start)
i2 = src.index(render_end_marker, i1)

new_render = r"""      function renderConiCoppetteGallery(rows){
        if(!rows || !rows.length) return '';

        const zoomIcon = `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false">
                   <polyline points="15 3 21 3 21 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                   <polyline points="9 21 3 21 3 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                   <line x1="21" y1="3" x2="14" y2="10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                   <line x1="3" y1="21" x2="10" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                 </svg>`;

        /* -- Coppette cards (cups) -- */
        const coppetteRows = rows.filter(([name]) => COPPETTE_ZONE_ORDER.indexOf(name) !== -1);
        const coppetteCards = COPPETTE_ZONE_ORDER.map((name, idx) => {
          const row = coppetteRows.find(r => r[0] === name);
          const src = CONI_COPPETTE_IMAGES[name];
          if(!src) return '';
          const imageSrc = encodeURI(src);
          const localName = getConiCoppetteDesc(name) || name;
          const zoomSrc = CONI_COPPETTE_ZOOM_IMAGES[name] || src;
          const slidesAttr = ` data-zoom-slides='${JSON.stringify([zoomSrc, src])}'`;
          return `
            <article class="pezziduri-card" data-coppette-card-id="${name}" role="button" tabindex="0" aria-expanded="false" style="--stagger-i:${idx}">
              <div class="pezziduri-media">
                <img src="${imageSrc}" alt="${localName}" loading="lazy" decoding="async" />
                <button class="card-zoom" type="button" aria-label="${t('b2b.zoom')}" data-zoom-src="${encodeURI(zoomSrc)}" data-zoom-alt="${localName}"${slidesAttr}>${zoomIcon}</button>
              </div>
              <div class="pezziduri-body">
                <div class="pezziduri-title">${localName}</div>
              </div>
            </article>
          `;
        }).join('');

        /* -- Coni cards (regular cones) -- */
        const coniRows = rows.filter(([name]) => name.indexOf('Gluten free') === -1 && COPPETTE_ZONE_ORDER.indexOf(name) === -1);
        const coniCards = CONI_ZONE_ORDER.map((name, idx) => {
          const src = CONI_COPPETTE_IMAGES[name];
          if(!src) return '';
          const imageSrc = encodeURI(src);
          const localName = getConiName(name);
          const zoomSrc = CONI_COPPETTE_ZOOM_IMAGES[name] || src;
          const slidesAttr = ` data-zoom-slides='${JSON.stringify([zoomSrc, src])}'`;
          return `
            <article class="pezziduri-card" data-coni-card-id="${name}" role="button" tabindex="0" aria-expanded="false" style="--stagger-i:${idx}">
              <div class="pezziduri-media">
                <img src="${imageSrc}" alt="${localName}" loading="lazy" decoding="async" />
                <button class="card-zoom" type="button" aria-label="${t('b2b.zoom')}" data-zoom-src="${encodeURI(zoomSrc)}" data-zoom-alt="${localName}"${slidesAttr}>${zoomIcon}</button>
              </div>
              <div class="pezziduri-body">
                <div class="pezziduri-title">${localName}</div>
              </div>
            </article>
          `;
        }).join('');

        /* -- Coni Gluten Free cards -- */
        const conigfCards = CONIGF_ZONE_ORDER.map((name, idx) => {
          const src = CONIGF_IMAGES[name];
          if(!src) return '';
          const imageSrc = encodeURI(src);
          const shortName = CONIGF_SHORT_NAMES[name] || name;
          const localName = getConiName(shortName);
          const zoomSrc = CONIGF_ZOOM_IMAGES[name] || src;
          const slidesAttr = ` data-zoom-slides='${JSON.stringify([zoomSrc, src])}'`;
          return `
            <article class="pezziduri-card" data-conigf-card-id="${name}" role="button" tabindex="0" aria-expanded="false" style="--stagger-i:${idx}">
              <div class="pezziduri-media">
                <img src="${imageSrc}" alt="${localName}" loading="lazy" decoding="async" />
                <button class="card-zoom" type="button" aria-label="${t('b2b.zoom')}" data-zoom-src="${encodeURI(zoomSrc)}" data-zoom-alt="${localName}"${slidesAttr}>${zoomIcon}</button>
              </div>
              <div class="pezziduri-body">
                <div class="pezziduri-title">${localName}</div>
              </div>
            </article>
          `;
        }).join('');

        return `
          <div class="modal__section">
            <div class="pezziduri-grid-stage">
              <h4>${t('b2b.coppette.sectionTitle')}</h4>
              <div class="pezziduri-grid">${coppetteCards}</div>
            </div>
          </div>
          <div class="modal__section">
            <div class="pezziduri-grid-stage">
              <h4>${t('b2b.coni.sectionTitle')}</h4>
              <div class="pezziduri-grid">${coniCards}</div>
            </div>
          </div>
          <div class="modal__section">
            <div class="pezziduri-grid-stage">
              <h4>${t('b2b.conigf.sectionTitle')}</h4>
              <div class="pezziduri-grid">${conigfCards}</div>
            </div>
          </div>
        `;
      }

"""

src = src[:i1] + new_render + src[i2:]
print("3. Replaced renderConiCoppetteGallery with card-grid version")

# ──────────────────────────────────────────────────────────────
# 4. Replace setupCoppetteInteraction + setupConiGfInteraction
#    + setupConiHeroInteraction with DOM-patching card handlers
# ──────────────────────────────────────────────────────────────
old_setup_start = "      function setupCoppetteInteraction(){"
old_setup_end = "      function renderAccessoriGallery(rows){"
i3 = src.index(old_setup_start)
i4 = src.index(old_setup_end, i3)

new_setup = r"""      function setupCoppetteInteraction(){
        const cards = defaultContent ? defaultContent.querySelectorAll('.pezziduri-card[data-coppette-card-id]') : [];
        cards.forEach((card) => {
          const id = card.dataset.coppetteCardId;
          if(!id) return;
          function handleCoppetteSelect(){
            const wasExpanded = expandedCoppetteId === id;
            if(expandedCoppetteId){
              const prev = defaultContent.querySelector('.pezziduri-card[data-coppette-card-id].is-expanded');
              if(prev){ prev.classList.remove('is-expanded'); prev.setAttribute('aria-expanded','false'); const o = prev.querySelector('.pezziduri-card__exp-body'); if(o) o.remove(); }
            }
            if(wasExpanded){ expandedCoppetteId = ''; return; }
            expandedCoppetteId = id;
            card.classList.add('is-expanded');
            card.setAttribute('aria-expanded','true');
            const data = CATEGORY_DATA['CONI_COPPETTE'];
            const row = data && data.rows ? data.rows.find(r => r[0] === id) : null;
            const localName = getConiCoppetteDesc(id) || id;
            const code = row ? row[1] : '';
            const capacity = row ? row[2] : '';
            const pack = row ? (row[3] || '') : '';
            const expBody = document.createElement('div');
            expBody.className = 'pezziduri-card__exp-body';
            expBody.innerHTML = `
              <div class="pezziduri-card__exp-header">
                <div><div class="pezziduri-card__exp-name">${localName}</div></div>
                <button class="pezziduri-card__exp-close" type="button" aria-label="Chiudi">&#x2715;</button>
              </div>
              <div class="pezziduri-card__exp-meta">
                <span><strong>${t('b2b.coppette.code')}</strong> ${code}</span>
                <span><strong>${t('b2b.coppette.capacity')}</strong> ${capacity}</span>
                ${pack ? `<span><strong>${t('b2b.coppette.packaging')}</strong> ${pack}</span>` : ''}
              </div>`;
            card.appendChild(expBody);
            const closeBtn = expBody.querySelector('.pezziduri-card__exp-close');
            if(closeBtn){ closeBtn.addEventListener('click', (e) => { e.stopPropagation(); handleCoppetteSelect(); }); }
            requestAnimationFrame(() => { requestAnimationFrame(() => { card.scrollIntoView({ behavior: 'smooth', block: 'center' }); }); });
          }
          card.addEventListener('click', (e) => { if(e.target.closest('.card-zoom')) return; handleCoppetteSelect(); });
          card.addEventListener('keydown', (e) => { if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); handleCoppetteSelect(); } });
        });
      }

      function setupConiCardInteraction(){
        const cards = defaultContent ? defaultContent.querySelectorAll('.pezziduri-card[data-coni-card-id]') : [];
        cards.forEach((card) => {
          const id = card.dataset.coniCardId;
          if(!id) return;
          function handleConiSelect(){
            const wasExpanded = expandedConiCardId === id;
            if(expandedConiCardId){
              const prev = defaultContent.querySelector('.pezziduri-card[data-coni-card-id].is-expanded');
              if(prev){ prev.classList.remove('is-expanded'); prev.setAttribute('aria-expanded','false'); const o = prev.querySelector('.pezziduri-card__exp-body'); if(o) o.remove(); }
            }
            if(wasExpanded){ expandedConiCardId = ''; return; }
            expandedConiCardId = id;
            card.classList.add('is-expanded');
            card.setAttribute('aria-expanded','true');
            const data = CATEGORY_DATA['CONI_COPPETTE'];
            const row = data && data.rows ? data.rows.find(r => r[0] === id) : null;
            const localName = getConiName(id);
            const desc = row ? (getConiCoppetteDesc(id) || row[1]) : '';
            const qty = row ? row[2] : '';
            const gf = getConiGfVariants()[id];
            const gfHtml = gf ? `
              <div style="margin-top:6px;width:100%;border-top:1px solid rgba(30,57,141,0.1);padding-top:8px">
                <div class="pezziduri-card__exp-section-label" style="color:#2e7d32">&#x1F33F; ${t('b2b.coni.gfVariant')}</div>
                <div class="pezziduri-card__exp-meta">
                  <span><strong>${gf.gfName}</strong></span>
                  <span>${gf.gfDesc} &mdash; ${gf.gfQty}</span>
                </div>
              </div>` : '';
            const expBody = document.createElement('div');
            expBody.className = 'pezziduri-card__exp-body';
            expBody.innerHTML = `
              <div class="pezziduri-card__exp-header">
                <div><div class="pezziduri-card__exp-name">${localName}</div></div>
                <button class="pezziduri-card__exp-close" type="button" aria-label="Chiudi">&#x2715;</button>
              </div>
              <div class="pezziduri-card__exp-meta">
                <span><strong>${t('b2b.coni.dimensions')}</strong> ${desc}</span>
                <span><strong>${t('b2b.coni.quantity')}</strong> ${qty}</span>
              </div>
              ${gfHtml}`;
            card.appendChild(expBody);
            const closeBtn = expBody.querySelector('.pezziduri-card__exp-close');
            if(closeBtn){ closeBtn.addEventListener('click', (e) => { e.stopPropagation(); handleConiSelect(); }); }
            requestAnimationFrame(() => { requestAnimationFrame(() => { card.scrollIntoView({ behavior: 'smooth', block: 'center' }); }); });
          }
          card.addEventListener('click', (e) => { if(e.target.closest('.card-zoom')) return; handleConiSelect(); });
          card.addEventListener('keydown', (e) => { if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); handleConiSelect(); } });
        });
      }

      function setupConigfCardInteraction(){
        const cards = defaultContent ? defaultContent.querySelectorAll('.pezziduri-card[data-conigf-card-id]') : [];
        cards.forEach((card) => {
          const id = card.dataset.conigfCardId;
          if(!id) return;
          function handleConigfSelect(){
            const wasExpanded = expandedConigfCardId === id;
            if(expandedConigfCardId){
              const prev = defaultContent.querySelector('.pezziduri-card[data-conigf-card-id].is-expanded');
              if(prev){ prev.classList.remove('is-expanded'); prev.setAttribute('aria-expanded','false'); const o = prev.querySelector('.pezziduri-card__exp-body'); if(o) o.remove(); }
            }
            if(wasExpanded){ expandedConigfCardId = ''; return; }
            expandedConigfCardId = id;
            card.classList.add('is-expanded');
            card.setAttribute('aria-expanded','true');
            const data = CATEGORY_DATA['CONI_COPPETTE'];
            const row = data && data.rows ? data.rows.find(r => r[0] === id) : null;
            const shortName = CONIGF_SHORT_NAMES[id] || id;
            const localName = getConiName(shortName);
            const desc = row ? (getConiCoppetteDesc(id) || row[1]) : '';
            const qty = row ? row[2] : '';
            const expBody = document.createElement('div');
            expBody.className = 'pezziduri-card__exp-body';
            expBody.innerHTML = `
              <div class="pezziduri-card__exp-header">
                <div><div class="pezziduri-card__exp-name">${localName}</div></div>
                <button class="pezziduri-card__exp-close" type="button" aria-label="Chiudi">&#x2715;</button>
              </div>
              <div class="pezziduri-card__exp-meta">
                <span><strong>${t('b2b.coni.dimensions')}</strong> ${desc}</span>
                <span><strong>${t('b2b.coni.quantity')}</strong> ${qty}</span>
              </div>`;
            card.appendChild(expBody);
            const closeBtn = expBody.querySelector('.pezziduri-card__exp-close');
            if(closeBtn){ closeBtn.addEventListener('click', (e) => { e.stopPropagation(); handleConigfSelect(); }); }
            requestAnimationFrame(() => { requestAnimationFrame(() => { card.scrollIntoView({ behavior: 'smooth', block: 'center' }); }); });
          }
          card.addEventListener('click', (e) => { if(e.target.closest('.card-zoom')) return; handleConigfSelect(); });
          card.addEventListener('keydown', (e) => { if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); handleConigfSelect(); } });
        });
      }

"""

src = src[:i3] + new_setup + src[i4:]
print("4. Replaced setup functions with DOM-patching card handlers")

# ──────────────────────────────────────────────────────────────
# 5. Add new state variables (expandedCoppetteId, expandedConiCardId, expandedConigfCardId)
#    and remove old state variables (selectedCoppetteId, selectedConiHeroId, selectedConiGfMapId)
# ──────────────────────────────────────────────────────────────
# Replace old state vars with new ones
src = src.replace("      let expandedConiId = new Set();\n", "      let expandedCoppetteId = '';\n      let expandedConiCardId = '';\n      let expandedConigfCardId = '';\n", 1)
src = src.replace("      let selectedCoppetteId = new Set();\n", "", 1)
src = src.replace("      let selectedConiHeroId = new Set();\n", "", 1)
src = src.replace("      let selectedConiGfMapId = new Set();\n", "", 1)
print("5. Replaced state variables")

# ──────────────────────────────────────────────────────────────
# 6. Update resetInteractiveSelections to reset new vars
# ──────────────────────────────────────────────────────────────
src = src.replace("        expandedConiId = new Set();", "        expandedCoppetteId = '';\n        expandedConiCardId = '';\n        expandedConigfCardId = '';", 1)
# Remove old resets
src = src.replace("        selectedCoppetteId = new Set();\n", "", 1)
src = src.replace("        selectedConiHeroId = new Set();\n", "", 1)
src = src.replace("        selectedConiGfMapId = new Set();\n", "", 1)
print("6. Updated resetInteractiveSelections")

# ──────────────────────────────────────────────────────────────
# 7. Update the CONI_COPPETTE setup call in renderCategoryContent
# ──────────────────────────────────────────────────────────────
old_setup_call = "if(category === 'CONI_COPPETTE'){ setupConiZoom(); setupCoppetteInteraction(); setupConiHeroInteraction(); setupConiGfInteraction(); }"
new_setup_call = "if(category === 'CONI_COPPETTE'){ setupCoppetteInteraction(); setupConiCardInteraction(); setupConigfCardInteraction(); }"
assert old_setup_call in src, "CONI_COPPETTE setup call not found"
src = src.replace(old_setup_call, new_setup_call, 1)
print("7. Updated renderCategoryContent setup calls")

# ──────────────────────────────────────────────────────────────
# 8. Remove setupConiZoom function (no longer needed)
# ──────────────────────────────────────────────────────────────
coni_zoom_pat = re.compile(
    r'\n      function setupConiZoom\(\)\{.*?\n      \}\n',
    re.DOTALL
)
m = coni_zoom_pat.search(src)
if m:
    src = src[:m.start()] + '\n' + src[m.end():]
    print(f"8. Removed setupConiZoom function ({m.end()-m.start()} chars)")
else:
    print("8. setupConiZoom already removed or not found")

# ──────────────────────────────────────────────────────────────
# Verify
# ──────────────────────────────────────────────────────────────
assert 'expandedConiId' not in src, "expandedConiId still present"
assert 'selectedCoppetteId' not in src, "selectedCoppetteId still present"
assert 'selectedConiHeroId' not in src, "selectedConiHeroId still present"
assert 'selectedConiGfMapId' not in src, "selectedConiGfMapId still present"
assert 'setupConiZoom' not in src, "setupConiZoom still present"
assert 'setupConiHeroInteraction' not in src, "setupConiHeroInteraction still present"
assert 'setupConiGfInteraction' not in src, "setupConiGfInteraction still present"
assert 'function renderConiCoppetteGallery' in src, "renderConiCoppetteGallery lost"
assert 'function setupCoppetteInteraction' in src, "setupCoppetteInteraction lost"
assert 'function setupConiCardInteraction' in src, "setupConiCardInteraction lost"
assert 'function setupConigfCardInteraction' in src, "setupConigfCardInteraction lost"
assert 'expandedCoppetteId' in src, "expandedCoppetteId not found"
assert 'expandedConiCardId' in src, "expandedConiCardId not found"
assert 'expandedConigfCardId' in src, "expandedConigfCardId not found"
assert 'CONI_COPPETTE_ZOOM_IMAGES' in src, "CONI_COPPETTE_ZOOM_IMAGES not found"
assert 'CONIGF_ZOOM_IMAGES' in src, "CONIGF_ZOOM_IMAGES not found"
assert 'pezziduri-grid' in src, "pezziduri-grid not found in coni section"
assert src.count('function setupCoppetteInteraction') == 1, "Duplicate setupCoppetteInteraction"

fp.write_text(src, encoding='utf-8')
new_len = len(src)
print(f"\nDone. {orig_len} -> {new_len} chars ({new_len - orig_len})")
print("All assertions passed.")
