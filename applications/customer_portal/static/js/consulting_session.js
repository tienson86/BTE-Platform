/* Attach the existing login to same-origin consulting requests, including built bundles. */
(function () {
  const nativeFetch = window.fetch.bind(window);
  window.fetch = function (input, options) {
    const url = new URL(typeof input === 'string' || input instanceof URL ? input : input.url, location.href);
    if (url.origin !== location.origin) return nativeFetch(input, options);
    if (url.pathname.startsWith('/backend/api/v1/consulting/')) {
      const headers = new Headers(options && options.headers || (input instanceof Request ? input.headers : undefined));
      const token = window.BtePortal.getToken();
      if (token) headers.set('Authorization', 'Bearer ' + token);
      return nativeFetch(input, Object.assign({}, options, {headers}));
    }
    const owner = new URLSearchParams(location.search).get('admin_owner');
    if (owner && /^\/backend\/api\/v1\/export\/(pdf|docx)$/.test(url.pathname) && options && typeof options.body === 'string') {
      const body = JSON.parse(options.body);
      body.admin_owner = owner;
      return nativeFetch(input, Object.assign({}, options, {body: JSON.stringify(body)}));
    }
    return nativeFetch(input, options);
  };
})();
