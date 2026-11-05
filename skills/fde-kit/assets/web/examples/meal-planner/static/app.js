/* Normal HTML forms remain the baseline; HTMX only replaces an interest card. */
document.addEventListener('htmx:beforeSwap', function (event) {
  const status = event.detail.xhr.status;
  if ([400, 401, 403, 404, 409, 422, 429].includes(status)) {
    const notice = document.getElementById('notice');
    if (notice) {
      event.detail.shouldSwap = true;
      event.detail.isError = false;
      event.detail.target = notice;
      event.detail.swapOverride = 'outerHTML';
    }
  }
});

document.addEventListener('htmx:afterSwap', function (event) {
  if (event.detail.target.id === 'notice') {
    const notice = document.getElementById('notice');
    if (notice) {
      notice.tabIndex = -1;
      notice.focus({ preventScroll: true });
      notice.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }
});

function showConnectionError() {
  const region = document.getElementById('notice');
  if (!region) return;
  const message = document.createElement('div');
  message.className = 'notice notice-error';
  message.setAttribute('role', 'alert');
  message.textContent = '연결을 확인하지 못했어요. 화면을 새로 열어 반영 여부를 확인한 뒤 다시 시도해 주세요.';
  region.replaceChildren(message);
  region.tabIndex = -1;
  region.focus({ preventScroll: true });
  region.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

document.addEventListener('htmx:sendError', showConnectionError);
document.addEventListener('htmx:timeout', showConnectionError);
document.addEventListener('htmx:responseError', function (event) {
  if (event.detail.xhr.status >= 500) showConnectionError();
});
