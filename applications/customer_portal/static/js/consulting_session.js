/* Attach the existing login to same-origin consulting requests, including built bundles. */
(function () {
  const nativeFetch = window.fetch.bind(window);
  function showQuotaWarning() {
    const main = document.getElementById("mainContent") || document.querySelector("main");
    if (!main) return;
    let alert = document.getElementById("quotaWarning");
    if (!alert) {
      alert = document.createElement("section");
      alert.id = "quotaWarning";
      alert.className = "member-quota-warning";
      alert.setAttribute("role", "alert");
      alert.tabIndex = -1;
      main.prepend(alert);
    }
    const title = document.createElement("strong");
    title.textContent = "Bạn đã dùng hết lượt cho công cụ này";
    const text = document.createElement("p");
    text.textContent = "Muốn tiếp tục xem ngay? Đổi 5 Linh Thạch lấy 1 lượt, hoặc xem cấp thành viên cao hơn để có thêm lượt cho những lần sau.";
    const wallet = document.createElement("a");
    wallet.href = "/linh-thach"; wallet.textContent = "Đổi lượt bằng Linh Thạch";
    const plans = document.createElement("a");
    plans.href = "/thanh-vien-bte"; plans.textContent = "Xem các cấp thành viên";
    const close = document.createElement("button");
    close.type = "button"; close.textContent = "Đóng";
    close.onclick = () => alert.remove();
    alert.replaceChildren(title, text, wallet, plans, close);
    alert.focus();
  }

  async function checkQuota(response) {
    if (response.status === 429) {
      const data = await response.clone().json().catch(() => null);
      if (data?.code === "quota_exhausted" || data?.errors?.some(error => error.code === "quota_exhausted")) showQuotaWarning();
    }
    return response;
  }

  window.fetch = function (input, options) {
    const url = new URL(typeof input === 'string' || input instanceof URL ? input : input.url, location.href);
    if (url.origin !== location.origin) return nativeFetch(input, options);
    if (url.pathname.startsWith('/backend/api/v1/consulting/')) {
      const headers = new Headers(options && options.headers || (input instanceof Request ? input.headers : undefined));
      const token = window.BtePortal.getToken();
      if (token) headers.set('Authorization', 'Bearer ' + token);
      return nativeFetch(input, Object.assign({}, options, {headers})).then(function(response) {
        const method = (options && options.method) || (input instanceof Request ? input.method : 'GET');
        if (response.ok && !['GET', 'HEAD', 'OPTIONS'].includes(method.toUpperCase())) window.dispatchEvent(new Event('bte:wallet-changed'));
        return checkQuota(response);
      });
    }
    const owner = new URLSearchParams(location.search).get('admin_owner');
    if (owner && /^\/backend\/api\/v1\/export\/(pdf|docx)$/.test(url.pathname) && options && typeof options.body === 'string') {
      const body = JSON.parse(options.body);
      body.admin_owner = owner;
      return nativeFetch(input, Object.assign({}, options, {body: JSON.stringify(body)}));
    }
    const response = nativeFetch(input, options);
    return url.pathname.startsWith("/backend/") ? response.then(checkQuota) : response;
  };
})();
