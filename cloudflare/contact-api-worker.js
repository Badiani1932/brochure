export default {
  async fetch(request, env) {
    const requestUrl = new URL(request.url);
    const origin = request.headers.get('Origin') || '';

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: buildCorsHeaders(origin, env) });
    }

    if (request.method === 'GET' && requestUrl.pathname === '/health') {
      return jsonResponse({ ok: true, service: 'badiani-contact-api' }, 200, origin, env);
    }

    if (request.method !== 'POST' || requestUrl.pathname !== '/send') {
      return jsonResponse({ error: 'Not Found' }, 404, origin, env);
    }

    if (!isOriginAllowed(origin, env)) {
      return jsonResponse({ error: 'Origin not allowed' }, 403, origin, env);
    }

    let payload;
    try {
      payload = await request.json();
    } catch {
      return jsonResponse({ error: 'Invalid JSON body' }, 400, origin, env);
    }

    const baseSubject = sanitizeOneLine((payload && payload.subject) || 'Richiesta contatto sito Badiani');
    const message = String((payload && (payload.message || payload.body)) || '').trim();

    if (!message) {
      return jsonResponse({ error: 'Missing message/body' }, 400, origin, env);
    }

    const toEmail = (env.MAIL_TO || '').trim();
    const fromEmail = (env.MAIL_FROM || '').trim();

    if (!toEmail || !fromEmail) {
      return jsonResponse({ error: 'MAIL_TO or MAIL_FROM not configured' }, 500, origin, env);
    }

    const data = extractBestData(payload);
    const requestType = classifyRequestType(payload, data);
    const subject = buildTaggedSubject(baseSubject, requestType, data);

    const requestId = crypto.randomUUID();
    const finalTextBody = buildCleanEmailBody(payload, message);
    const finalHtmlBody = buildProfessionalEmailHtml(payload, message, env);
    const replyTo = inferReplyTo(payload);

    try {
      await sendResend({
        apiKey: env.RESEND_API_KEY,
        fromEmail,
        toEmail,
        subject,
        bodyText: finalTextBody,
        bodyHtml: finalHtmlBody,
        replyTo
      });

      return jsonResponse({ ok: true, requestId }, 200, origin, env);
    } catch (error) {
      console.error('send-email-error', (error && error.message) || error);
      return jsonResponse({ error: 'Email send failed', details: String((error && error.message) || error) }, 502, origin, env);
    }
  }
};

function sanitizeOneLine(input) {
  return String(input || '').replace(/[\r\n]+/g, ' ').trim().slice(0, 200) || 'Richiesta contatto sito Badiani';
}

function buildTaggedSubject(baseSubject, requestType, data) {
  const clean = sanitizeOneLine(baseSubject);
  const tagMap = {
    corporate: '[B2B]',
    eventi: '[EVENTI]',
    general: '[WEB]'
  };

  const tag = tagMap[requestType] || tagMap.general;
  const urgent = isUrgentRequest(requestType, data) ? '[URGENTE]' : '';

  const normalized = clean
    .replace(/^\[(?:B2B|EVENTI|WEB)\]\s*/i, '')
    .replace(/^\[URGENTE\]\s*/i, '')
    .trim();

  const prefix = `${tag}${urgent}`;
  return `${prefix} ${normalized}`.trim();
}

function isUrgentRequest(requestType, data) {
  if (requestType !== 'eventi' || !data || typeof data !== 'object') return false;

  const eventDate = parseDateValue(data.data);
  if (!eventDate) return false;

  const now = new Date();
  const today = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
  const diffMs = eventDate.getTime() - today.getTime();
  const diffDays = Math.floor(diffMs / 86400000);

  return diffDays >= 0 && diffDays <= 7;
}

function parseDateValue(value) {
  const raw = String(value || '').trim();
  if (!raw) return null;

  const match = raw.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!match) return null;

  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  if (!year || !month || !day) return null;

  return new Date(Date.UTC(year, month - 1, day));
}

function buildCleanEmailBody(payload, fallbackMessage) {
  const lines = [];
  lines.push('Nuova richiesta dal sito Badiani');
  lines.push('');

  const source = sanitizeOneLine((payload && payload.source) || 'website');
  const formId = sanitizeOneLine((payload && payload.formId) || '');
  if (source && source !== 'website') lines.push(`Canale: ${source}`);
  if (formId) lines.push(`Form: ${formId}`);

  const data = extractBestData(payload);
  const entries = toDisplayEntries(data);
  if (entries.length) {
    if (lines[lines.length - 1] !== '') lines.push('');
    lines.push('Dettagli richiesta:');
    entries.forEach(({ label, value }) => {
      if (Array.isArray(value)) {
        if (!value.length) return;
        lines.push(`${label}:`);
        value.forEach((item) => lines.push(`- ${item}`));
      } else {
        lines.push(`${label}: ${value}`);
      }
    });
  }

  const extraMessage = sanitizeMessageForEmail(fallbackMessage);
  if (extraMessage) {
    if (lines[lines.length - 1] !== '') lines.push('');
    lines.push('Messaggio:');
    lines.push(extraMessage);
  }

  return lines.join('\n').trim();
}

function buildProfessionalEmailHtml(payload, fallbackMessage, env) {
  const source = sanitizeOneLine((payload && payload.source) || 'website');
  const formId = sanitizeOneLine((payload && payload.formId) || '');
  const logoUrl = sanitizeOneLine((env && env.MAIL_LOGO_URL) || 'https://badiani1932.github.io/badianibroshure/assets/images/branding/logo-white.png');

  const data = extractBestData(payload);
  const requestType = classifyRequestType(payload, data);
  const theme = getEmailTheme(requestType);
  const entries = toDisplayEntries(data);
  const extraMessage = sanitizeMessageForEmail(fallbackMessage);

  const detailsRows = entries.map(({ label, value }) => {
    const labelHtml = escapeHtml(label);
    if (Array.isArray(value)) {
      const list = value.map((item) => `<li style="margin:0 0 4px 0;">${escapeHtml(item)}</li>`).join('');
      return `
        <tr>
          <td style="padding:10px 0;vertical-align:top;width:220px;font-weight:700;color:${theme.accent};text-transform:uppercase;letter-spacing:.5px;font-size:12px;">${labelHtml}</td>
          <td style="padding:10px 0;vertical-align:top;color:${theme.text};font-size:14px;">
            <ul style="margin:0;padding-left:18px;">${list}</ul>
          </td>
        </tr>`;
    }

    return `
      <tr>
        <td style="padding:10px 0;vertical-align:top;width:220px;font-weight:700;color:${theme.accent};text-transform:uppercase;letter-spacing:.5px;font-size:12px;">${labelHtml}</td>
        <td style="padding:10px 0;vertical-align:top;color:${theme.text};font-size:14px;">${escapeHtml(value)}</td>
      </tr>`;
  }).join('');

  const sourceInfo = [
    source && source !== 'website' ? `<span style="margin-right:14px;"><strong>Canale:</strong> ${escapeHtml(source)}</span>` : '',
    formId ? `<span><strong>Form:</strong> ${escapeHtml(formId)}</span>` : ''
  ].filter(Boolean).join('');

  const compactInfo = buildCompactInfo(requestType, data);
  const compactInfoHtml = compactInfo.length
    ? `<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:0 0 16px 0;">${compactInfo.map((item) => `
      <div style="padding:12px;background:${theme.cardBg};border:1px solid ${theme.cardBorder};border-radius:0;">
        <div style="font-size:11px;letter-spacing:.6px;text-transform:uppercase;color:${theme.muted};font-weight:700;">${escapeHtml(item.label)}</div>
        <div style="margin-top:6px;font-size:14px;line-height:1.4;color:${theme.text};font-weight:600;">${escapeHtml(item.value)}</div>
      </div>`).join('')}</div>`
    : '';

  const messageBlock = extraMessage
    ? `
      <div style="margin-top:24px;padding:16px 18px;background:${theme.cardBg};border:1px solid ${theme.cardBorder};border-radius:0;">
        <div style="font-size:14px;font-weight:700;color:${theme.accent};margin-bottom:8px;">Messaggio</div>
        <div style="font-size:14px;line-height:1.7;color:${theme.text};white-space:pre-line;">${escapeHtml(extraMessage)}</div>
      </div>`
    : '';

  return `<!doctype html>
<html lang="it">
  <body style="margin:0;padding:0;background:${theme.pageBg};font-family:'SuperGroteskDigits','SuperGroteskA','SuperGroteskB',Arial,'Helvetica Neue',Helvetica,sans-serif;color:${theme.text};">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:${theme.pageBg};padding:24px 12px;">
      <tr>
        <td align="center">
          <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:760px;background:#ffffff;border-radius:0;overflow:hidden;border:1px solid ${theme.cardBorder};">
            <tr>
              <td style="background:${theme.headerBg};padding:22px 20px;text-align:center;">
                <img src="${escapeHtml(logoUrl)}" alt="Badiani 1932" width="220" style="display:block;margin:0 auto;max-width:220px;height:auto;border:0;outline:none;text-decoration:none;" />
              </td>
            </tr>
            <tr>
              <td style="padding:24px 26px 12px 26px;">
                <div style="display:flex;align-items:center;gap:10px;margin:0 0 8px 0;">
                  <span style="display:inline-block;width:10px;height:10px;background:${theme.pink};"></span>
                  <span style="font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:${theme.muted};font-weight:700;">Badiani 1932</span>
                </div>
                <h1 style="margin:0;font-size:22px;line-height:1.3;color:${theme.accent};text-transform:uppercase;letter-spacing:.8px;">${escapeHtml(theme.title)}</h1>
                ${sourceInfo ? `<p style="margin:10px 0 0 0;font-size:13px;line-height:1.6;color:${theme.muted};">${sourceInfo}</p>` : ''}
              </td>
            </tr>
            <tr>
              <td style="padding:8px 26px 24px 26px;">
                <div style="height:2px;background:linear-gradient(90deg, ${theme.pink} 0%, ${theme.accent} 45%, ${theme.cyan} 100%);margin:0 0 18px 0;"></div>
                ${compactInfoHtml}
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse;">
                  ${detailsRows || '<tr><td style="padding:10px 0;color:#64748b;">Nessun dettaglio disponibile.</td></tr>'}
                </table>
                ${messageBlock}
              </td>
            </tr>
            <tr>
              <td style="padding:14px 26px 20px 26px;border-top:1px solid ${theme.cardBorder};font-size:12px;line-height:1.6;color:${theme.muted};">
                Email generata automaticamente dal modulo contatti del sito Badiani — Gelato artigianale dal 1932.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>`;
}

function classifyRequestType(payload, data) {
  const source = String((payload && payload.source) || '').toLowerCase();
  const formId = String((payload && payload.formId) || '').toLowerCase();
  const interest = String(data.interesse || '').toLowerCase();

  if (source.includes('b2b') || formId.includes('b2b') || data.azienda || data.tipoAzienda || data.partitaIva) {
    return 'corporate';
  }

  if (
    source.includes('event') || source.includes('tosinghi') || source.includes('esterno') ||
    formId.includes('tosinghi') || formId.includes('external') || formId.includes('event') ||
    interest.includes('event')
  ) {
    return 'eventi';
  }

  return 'general';
}

function getEmailTheme(type) {
  if (type === 'corporate') {
    return {
      title: 'Nuova richiesta Corporate B2B',
      headerBg: '#0f274f',
      accent: '#0f274f',
      pageBg: '#eef2f7',
      cardBg: '#f6f8fc',
      cardBorder: '#d7deea',
      pink: '#f067a6',
      cyan: '#5B9AAD',
      text: '#1f2937',
      muted: '#5f6b7a'
    };
  }

  if (type === 'eventi') {
    return {
      title: 'Nuova richiesta Eventi',
      headerBg: '#1e398d',
      accent: '#1e398d',
      pageBg: '#f3f5f8',
      cardBg: '#f8fafc',
      cardBorder: '#e5e7eb',
      pink: '#f067a6',
      cyan: '#5B9AAD',
      text: '#1f2937',
      muted: '#64748b'
    };
  }

  return {
    title: 'Nuova richiesta dal sito',
    headerBg: '#1e398d',
    accent: '#1e398d',
    pageBg: '#f3f5f8',
    cardBg: '#f8fafc',
    cardBorder: '#e5e7eb',
    pink: '#f067a6',
    cyan: '#5B9AAD',
    text: '#1f2937',
    muted: '#64748b'
  };
}

function firstNotEmpty(...values) {
  for (const value of values) {
    const str = String(value || '').trim();
    if (str) return str;
  }
  return '';
}

function buildCompactInfo(type, data) {
  if (type === 'corporate') {
    return [
      { label: 'Azienda', value: firstNotEmpty(data.azienda) },
      { label: 'Contatto', value: firstNotEmpty([data.nome, data.cognome].filter(Boolean).join(' ')) },
      { label: 'Email', value: firstNotEmpty(data.email) },
      { label: 'Telefono', value: firstNotEmpty(data.telefono) }
    ].filter((item) => item.value);
  }

  if (type === 'eventi') {
    return [
      { label: 'Cliente', value: firstNotEmpty([data.nome, data.cognome].filter(Boolean).join(' ')) },
      { label: 'Data evento', value: firstNotEmpty(data.data) },
      { label: 'Numero persone', value: firstNotEmpty(data.persone) },
      { label: 'Telefono', value: firstNotEmpty(data.telefono) }
    ].filter((item) => item.value);
  }

  return [
    { label: 'Contatto', value: firstNotEmpty([data.nome, data.cognome].filter(Boolean).join(' ')) },
    { label: 'Email', value: firstNotEmpty(data.email) },
    { label: 'Telefono', value: firstNotEmpty(data.telefono) }
  ].filter((item) => item.value);
}

function extractBestData(payload) {
  if (payload && payload.structured && typeof payload.structured === 'object') {
    return payload.structured;
  }

  if (payload && payload.fields && typeof payload.fields === 'object') {
    const normalized = {};
    Object.entries(payload.fields).forEach(([key, value]) => {
      const cleanKey = String(key || '').replace(/\[\]$/g, '');
      normalized[cleanKey] = value;
    });
    return normalized;
  }

  return {};
}

function toDisplayEntries(data) {
  const labelMap = {
    nome: 'Nome',
    cognome: 'Cognome',
    email: 'Email',
    telefono: 'Telefono',
    tipo: 'Azienda o Privato',
    azienda: 'Azienda',
    tipoAzienda: 'Tipo Attività',
    partitaIva: 'Partita IVA',
    preferenza: 'Preferenza di contatto',
    preferenzaContatto: 'Preferenza di contatto',
    data: 'Data evento',
    orario: 'Orario',
    persone: 'Numero persone',
    interesse: 'Interesse',
    extra: 'Opzioni extra',
    extras: 'Dettaglio opzioni extra',
    eventi: 'Evento di interesse',
    messaggio: 'Messaggio'
  };

  const priorityOrder = [
    'nome', 'cognome', 'email', 'telefono', 'tipo', 'azienda', 'tipoAzienda', 'partitaIva',
    'preferenzaContatto', 'preferenza', 'data', 'orario', 'persone', 'interesse', 'extra',
    'extras', 'eventi', 'messaggio'
  ];

  const used = new Set();
  const entries = [];

  priorityOrder.forEach((key) => {
    if (!Object.prototype.hasOwnProperty.call(data, key)) return;
    const value = normalizeDisplayValue(data[key]);
    if (isEmptyValue(value)) return;
    entries.push({ label: labelMap[key] || key, value });
    used.add(key);
  });

  Object.entries(data).forEach(([key, rawValue]) => {
    if (used.has(key)) return;
    const value = normalizeDisplayValue(rawValue);
    if (isEmptyValue(value)) return;
    const fallbackLabel = labelMap[key] || key;
    entries.push({ label: fallbackLabel, value });
  });

  return entries;
}

function normalizeDisplayValue(value) {
  if (Array.isArray(value)) {
    return value
      .map((item) => String(item || '').trim())
      .filter(Boolean);
  }

  return String(value || '').trim();
}

function isEmptyValue(value) {
  if (Array.isArray(value)) return value.length === 0;
  return !String(value || '').trim();
}

function sanitizeMessageForEmail(message) {
  const raw = String(message || '').trim();
  if (!raw) return '';

  const cleaned = raw
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !/^===/.test(line) && !/^---/.test(line))
    .join('\n')
    .trim();

  return cleaned;
}

function inferReplyTo(payload) {
  const fromStructured = payload && payload.structured ? payload.structured.email : '';
  if (fromStructured && typeof fromStructured === 'string' && fromStructured.includes('@')) return fromStructured.trim();

  const fields = payload && payload.fields ? payload.fields : null;
  if (fields && typeof fields === 'object') {
    const candidate = fields.email;
    if (typeof candidate === 'string' && candidate.includes('@')) return candidate.trim();
  }

  return '';
}

function safePretty(value) {
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
}

async function sendResend({ apiKey, fromEmail, toEmail, subject, bodyText, bodyHtml, replyTo }) {
  if (!apiKey) throw new Error('Missing RESEND_API_KEY');

  const body = {
    from: `Badiani Website <${fromEmail}>`,
    to: [toEmail],
    subject,
    html: bodyHtml || undefined,
    text: bodyText || undefined
  };

  if (replyTo) body.reply_to = replyTo;

  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(`Resend API error: ${response.status} ${safePretty(data)}`);
  }

  return data;
}

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function isOriginAllowed(origin, env) {
  if (!origin) return true;

  const raw = (env.ALLOWED_ORIGIN || '').trim();
  if (!raw) return true;

  const allowed = raw.split(',').map((x) => x.trim()).filter(Boolean);
  if (allowed.includes('*')) return true;
  return allowed.includes(origin);
}

function buildCorsHeaders(origin, env) {
  const headers = new Headers();

  const raw = (env.ALLOWED_ORIGIN || '').trim();
  if (!raw) {
    headers.set('Access-Control-Allow-Origin', origin || '*');
  } else if (raw.includes('*')) {
    headers.set('Access-Control-Allow-Origin', '*');
  } else {
    const allowed = raw.split(',').map((x) => x.trim()).filter(Boolean);
    if (origin && allowed.includes(origin)) {
      headers.set('Access-Control-Allow-Origin', origin);
      headers.set('Vary', 'Origin');
    }
  }

  headers.set('Access-Control-Allow-Methods', 'POST, OPTIONS, GET');
  headers.set('Access-Control-Allow-Headers', 'Content-Type');
  headers.set('Access-Control-Max-Age', '86400');
  return headers;
}

function jsonResponse(payload, status, origin, env) {
  const headers = buildCorsHeaders(origin, env);
  headers.set('Content-Type', 'application/json; charset=utf-8');
  return new Response(JSON.stringify(payload), { status, headers });
}
