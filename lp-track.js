/* Landing page tracking. Edit the three values below once, all pages pick them up.
   Leave a value empty and that part stays switched off. The only call to action
   on the pages is WhatsApp, so there is one conversion to track. Personalised
   ads signals are turned off on purpose: Google does not allow remarketing on
   health conditions. */
(function () {
  var CONFIG = {
    adsId: '',          // Google Ads tag, looks like AW-1234567890
    whatsappLabel: '',  // conversion label for the WhatsApp button
    ga4Id: ''           // optional, looks like G-XXXXXXXXXX
  };

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;

  var id = CONFIG.adsId || CONFIG.ga4Id;
  if (id) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    document.head.appendChild(s);
    gtag('js', new Date());
    if (CONFIG.adsId) gtag('config', CONFIG.adsId, { allow_ad_personalization_signals: false });
    if (CONFIG.ga4Id) gtag('config', CONFIG.ga4Id, { allow_google_signals: false, allow_ad_personalization_signals: false });
  }

  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-conv]') : null;
    if (!el || !id) return;
    var where = el.getAttribute('data-loc') || '';
    if (CONFIG.adsId && CONFIG.whatsappLabel) gtag('event', 'conversion', { send_to: CONFIG.adsId + '/' + CONFIG.whatsappLabel });
    gtag('event', 'whatsapp_click', { location: where });
  }, true);
})();
