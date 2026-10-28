// loopny.net contact form. The site posts each message here; this emails it on.
// To send to someone else, change SEND_TO and push a new version.
var SEND_TO = 'loopworkflow@gmail.com';
var MAX_PER_HOUR = 30;

function doPost(e) {
  var d = {};
  try {
    d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
  } catch (err) {
    d = (e && e.parameter) || {};
  }

  // Bots fill the hidden field or post in under 2 seconds. Tell them ok and drop it.
  if (d.website || Number(d.ms) < 2000) return reply({ ok: true });

  var name = clip(d.name, 100);
  var business = clip(d.business, 120);
  var phone = clip(d.phone, 40);
  var email = clip(d.email, 200);
  var message = clip(d.message, 5000);
  var goodEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  if (!name || !message || !(phone || goodEmail)) return reply({ ok: false, error: 'missing' });
  if (!underLimit()) return reply({ ok: false, error: 'busy' });

  var body = [
    'Name: ' + name,
    'Business: ' + (business || '-'),
    'Phone: ' + (phone || '-'),
    'Email: ' + (email || '-'),
    '',
    message,
    '',
    'Sent from ' + clip(d.page, 300) + ' at ' + new Date().toString()
  ].join('\n');

  var mail = {
    to: SEND_TO,
    subject: 'loopny.net: ' + name + (business ? ' (' + business + ')' : ''),
    body: body,
    name: 'loopny.net contact form'
  };
  if (goodEmail) mail.replyTo = email;
  MailApp.sendEmail(mail);

  return reply({ ok: true });
}

function doGet() {
  return reply({ ok: true, service: 'loopny.net contact form' });
}

// Run this once from the editor to grant the send-mail permission.
function authorize() {
  Logger.log('Emails left today: ' + MailApp.getRemainingDailyQuota());
}

function underLimit() {
  var cache = CacheService.getScriptCache();
  var key = 'count-' + Utilities.formatDate(new Date(), 'GMT', 'yyyyMMddHH');
  var n = Number(cache.get(key) || 0);
  if (n >= MAX_PER_HOUR) return false;
  cache.put(key, String(n + 1), 3600);
  return true;
}

function clip(v, max) {
  return String(v == null ? '' : v).replace(/\r/g, '').trim().slice(0, max);
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
