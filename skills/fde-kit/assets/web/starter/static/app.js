document.addEventListener('htmx:beforeSwap', function (event) {
  if ([400, 401, 403, 404, 409, 422, 429].includes(event.detail.xhr.status)) {
    const notice = document.getElementById('notice');
    if (notice) {
      event.detail.shouldSwap = true;
      event.detail.isError = false;
      event.detail.target = notice;
      event.detail.swapOverride = 'outerHTML';
    }
  }
});
