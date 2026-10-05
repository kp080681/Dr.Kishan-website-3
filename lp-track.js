/* Landing page tracking. Edit the four values below once, all pages pick them up.
   Leave a value empty and that part stays switched off. Personalised ads
   signals are turned off on purpose: Google does not allow remarketing on
   health conditions. */
(function () {
  var CONFIG = {
    adsId: '',          // Google Ads tag, looks like AW-1234567890
    callLabel: '',      // conversion label for the Call button
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
    var type = el.getAttribute('data-conv');
    var where = el.getAttribute('data-loc') || '';
    var label = type === 'call' ? CONFIG.callLabel : CONFIG.whatsappLabel;
    if (CONFIG.adsId && label) gtag('event', 'conversion', { send_to: CONFIG.adsId + '/' + label });
    gtag('event', type + '_click', { location: where });
  }, true);
})();
