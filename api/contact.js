// Vercel Serverless Function: nimmt das Kontaktformular entgegen und
// versendet die Anfrage per Postmark. Der Postmark-Server-Token liegt
// ausschließlich als Umgebungsvariable in Vercel (nie im Client-Code).

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ success: false, error: 'method_not_allowed' });
  }

  // Body robust parsen (Vercel parst JSON i.d.R. automatisch)
  var body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (e) { body = {}; }
  }
  body = body || {};

  // Honeypot: von Bots ausgefüllt -> still verwerfen, aber "success" melden
  if (body._honey) {
    return res.status(200).json({ success: true });
  }

  var name = (body.name || '').toString().trim();
  var email = (body.email || '').toString().trim();
  var company = (body.company || '').toString().trim();
  var message = (body.message || '').toString().trim();

  if (!name || !email || !message) {
    return res.status(400).json({ success: false, error: 'missing_fields' });
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ success: false, error: 'invalid_email' });
  }
  if (message.length > 8000) {
    return res.status(400).json({ success: false, error: 'too_long' });
  }

  var TOKEN = process.env.POSTMARK_TOKEN;
  var FROM = process.env.MAIL_FROM;                       // verifizierter Absender in Postmark
  var TO = process.env.MAIL_TO || 'info@leadesk.de';
  var STREAM = process.env.POSTMARK_STREAM || 'outbound';

  if (!TOKEN || !FROM) {
    return res.status(500).json({ success: false, error: 'not_configured' });
  }

  var subject = 'Neue Kontakt-/Demo-Anfrage über leadesk.de';
  var textBody =
    'Neue Anfrage über das Kontaktformular auf leadesk.de\n\n' +
    'Name: ' + name + '\n' +
    'E-Mail: ' + email + '\n' +
    'Unternehmen: ' + (company || '—') + '\n\n' +
    'Nachricht:\n' + message + '\n';
  var htmlBody =
    '<h2 style="margin:0 0 12px">Neue Kontakt-/Demo-Anfrage</h2>' +
    '<p style="margin:0 0 16px;color:#555">über das Kontaktformular auf leadesk.de</p>' +
    '<table cellpadding="6" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:14px">' +
    '<tr><td style="color:#888">Name</td><td><strong>' + escapeHtml(name) + '</strong></td></tr>' +
    '<tr><td style="color:#888">E-Mail</td><td><a href="mailto:' + escapeHtml(email) + '">' + escapeHtml(email) + '</a></td></tr>' +
    '<tr><td style="color:#888">Unternehmen</td><td>' + escapeHtml(company || '—') + '</td></tr>' +
    '</table>' +
    '<p style="margin:16px 0 6px;color:#888;font-family:Arial,sans-serif;font-size:14px">Nachricht</p>' +
    '<div style="white-space:pre-wrap;font-family:Arial,sans-serif;font-size:14px;line-height:1.5">' + escapeHtml(message) + '</div>';

  try {
    var pmRes = await fetch('https://api.postmarkapp.com/email', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Postmark-Server-Token': TOKEN
      },
      body: JSON.stringify({
        From: FROM,
        To: TO,
        ReplyTo: name ? (name + ' <' + email + '>') : email,
        Subject: subject,
        TextBody: textBody,
        HtmlBody: htmlBody,
        MessageStream: STREAM
      })
    });

    if (!pmRes.ok) {
      var errText = await pmRes.text();
      console.error('Postmark error', pmRes.status, errText);
      return res.status(502).json({ success: false, error: 'send_failed' });
    }

    return res.status(200).json({ success: true });
  } catch (e) {
    console.error('Contact function error', e);
    return res.status(500).json({ success: false, error: 'server_error' });
  }
};
