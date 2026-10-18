/* Landing page tracking. Google Tag Manager (container in the page head) owns the tags.
   This file only tells it when a patient taps a WhatsApp button, by pushing a
   "whatsapp_click" event into the dataLayer. In Tag Manager, use a Custom Event
   trigger named whatsapp_click for the Google Ads conversion tag.
   Personalised ads signals and remarketing stay off on purpose: Google does not
   allow remarketing on health conditions. */
(function () {
  window.dataLayer = window.dataLayer || [];
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-conv]') : null;
    if (!el) return;
    window.dataLayer.push({
      event: 'whatsapp_click',
      click_location: el.getAttribute('data-loc') || ''
    });
  }, true);
})();
