(function () {
  const editor = document.getElementById('menuVisibilityEditor');
  const path = '/api/v1/portal-menu-visibility';
  if (!editor) {
    fetch('/backend' + path, {cache: 'no-store'})
      .then(response => response.ok ? response.json() : Promise.reject())
      .then(({hidden}) => {
        for (const [position, container] of [['horizontal', 'appNav'], ['vertical', 'memberSidebar']]) {
          const links = document.querySelectorAll('#' + container + ' a[href]');
          for (const link of links) {
            if (hidden[position].includes(link.getAttribute('href'))) link.remove();
          }
        }
      }).catch(() => {});
    return;
  }
  const api = window.BteAdmin;
  const state = document.getElementById('menuVisibilityState');
  const button = editor.querySelector('button');
  const groups = {horizontal: 'Menu ngang', vertical: 'Menu dọc thành viên'};
  api.get(path).then(({links, hidden}) => {
    for (const [position, caption] of Object.entries(groups)) {
      const group = editor.querySelector('[data-menu-group="' + position + '"]');
      const heading = document.createElement('legend');
      heading.textContent = caption;
      group.append(heading);
      for (const [url, title] of Object.entries(links[position])) {
        const label = document.createElement('label');
        label.className = 'course-check';
        const box = document.createElement('input');
        box.type = 'checkbox';
        box.name = position;
        box.value = url;
        box.checked = !hidden[position].includes(url);
        label.append(box, document.createTextNode(title));
        group.append(label);
      }
    }
    state.textContent = '';
    button.disabled = false;
  }).catch(error => { state.textContent = error.message; });
  editor.onsubmit = async event => {
    event.preventDefault();
    button.disabled = true;
    const hidden = {};
    for (const position of Object.keys(groups)) {
      hidden[position] = [...editor.querySelectorAll('input[name="' + position + '"]:not(:checked)')].map(box => box.value);
    }
    try {
      await api.put('/api/v1/admin/portal-menu-visibility', hidden);
      state.textContent = 'Đã lưu. Tải lại trang thành viên để xem menu.';
    } catch (error) {
      state.textContent = error.message;
    } finally {
      button.disabled = false;
    }
  };
})();
