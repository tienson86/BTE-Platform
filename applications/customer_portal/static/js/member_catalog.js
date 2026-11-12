(function () {
  const root = document.querySelector('[data-member-catalog]');
  if (!root) return;
  const admin = root.dataset.memberCatalog === 'admin';
  const api = admin ? window.BteAdmin : window.BtePortal;
  const routes = {
    'khoa-hoc-offline': 'offline', 'offline-courses': 'offline',
    'shop-vat-pham': 'shop', 'member-shop': 'shop',
    'thong-bao-noi-bo': 'notices', 'member-notices': 'notices',
  };
  const kind = routes[location.pathname.split('/').filter(Boolean).pop()];
  const shop = kind === 'shop', notices = kind === 'notices';
  const title = {offline: 'Khóa học Offline', shop: 'Shop Vật phẩm', notices: 'Thông báo Nội bộ'}[kind];
  const endpoint = '/api/v1/' + (admin ? 'admin/' : '') + 'member-catalog/' + kind;
  const host = document.getElementById('memberCatalogContent');
  const state = document.getElementById('memberCatalogState');
  document.getElementById('memberCatalogTitle').textContent = title;
  const money = new Intl.NumberFormat('vi-VN', {style: 'currency', currency: 'VND'});
  const statuses = {pending: 'Chờ xử lý', confirmed: 'Đã xác nhận mua hàng', cancelled: 'Đã hủy'};
  const formatDate = value => value.split('-').reverse().join('/');
  function el(tag, content, css) {
    const node = document.createElement(tag);
    if (content !== undefined) node.textContent = content;
    if (css) node.className = css;
    return node;
  }
  function field(form, name, caption, options = {}) {
    const label = el('label', caption, options.wide ? 'course-wide' : '');
    const input = el(options.choices ? 'select' : options.multiline ? 'textarea' : 'input');
    if (input.tagName === 'INPUT') input.type = options.type || 'text';
    if (options.choices) {
      for (const [value, text] of Object.entries(options.choices)) {
        const option = el('option', text);
        option.value = value;
        input.append(option);
      }
    }
    for (const prop of ['min', 'max', 'maxLength', 'required', 'pattern', 'autocomplete', 'placeholder', 'inputMode']) {
      if (options[prop] !== undefined) input[prop] = options[prop];
    }
    if (options.choices) {
      for (const option of input.options) option.defaultSelected = option.value === options.value;
    } else if (!['file', 'checkbox'].includes(input.type)) {
      input.defaultValue = options.value ?? '';
    }
    input.name = name;
    label.append(input);
    form.append(label);
    return input;
  }
  function wire(form, caption, save) {
    const button = el('button', caption, 'course-action');
    button.type = 'submit';
    const message = el('p', undefined, 'course-wide');
    message.setAttribute('role', 'status');
    form.append(button, message);
    form.addEventListener('submit', async event => {
      event.preventDefault();
      button.disabled = true;
      message.classList.remove('course-error');
      message.textContent = 'Đang gửi…';
      try {
        await save(message);
      } catch (error) {
        message.classList.add('course-error');
        message.textContent = error.message;
      } finally {
        button.disabled = false;
      }
    });
  }
  const imageTypes = ['image/jpeg', 'image/png', 'image/webp'];
  const coverEndpoint = '/api/v1/member-catalog/' + kind;
  function readCover(file) {
    if (!imageTypes.includes(file.type) || file.size > 3 * 1024 * 1024) {
      return Promise.reject(new Error('Chọn ảnh JPG, PNG hoặc WebP tối đa 3 MB.'));
    }
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject(new Error('Không đọc được tệp ảnh.'));
      reader.readAsDataURL(file);
    });
  }
  function showCover(image, item, stillRelevant = () => true) {
    if (!item.has_cover) return;
    api.get(coverEndpoint + '/' + item.id + '/cover').then(data => {
      if (!stillRelevant()) return;
      image.src = data.cover;
      image.hidden = false;
    }).catch(() => {});
  }
  function listingEditor(item, onCreate) {
    const editor = el('details');
    const heading = el('summary');
    function updateHeading() {
      heading.textContent = item.id ? item.title + ' · ' + (item.published ? 'Đã đăng' : 'Bản nháp') : 'Thêm mới';
    }
    updateHeading();
    const form = el('form', undefined, 'course-form');
    field(form, 'title', 'Tiêu đề', {value: item.title, maxLength: 200, required: true, wide: true});
    field(form, 'body', 'Nội dung', {value: item.body, multiline: true, maxLength: 60000, required: true, wide: true}).rows = 7;
    let file, remove, preview;
    if (shop || notices) {
      file = field(form, 'cover_file', 'Ảnh bìa (JPG, PNG, WebP · tối đa 3 MB)', {type: 'file', wide: true});
      file.accept = imageTypes.join(',');
      remove = field(form, 'remove_cover', 'Xóa ảnh bìa hiện tại', {type: 'checkbox', wide: true});
      remove.parentElement.classList.add('course-check');
      preview = el('img', undefined, 'catalog-cover catalog-cover-preview course-wide');
      preview.alt = 'Xem trước ảnh bìa';
      preview.hidden = true;
      form.append(preview);
      editor.addEventListener('toggle', () => {
        if (editor.open && !file.files.length && !remove.checked && !preview.src) showCover(preview, item, () => !file.files.length && !remove.checked);
      });
      file.onchange = async () => {
        file.setCustomValidity('');
        if (!file.files.length) {
          preview.removeAttribute('src');
          preview.hidden = true;
          if (!remove.checked) showCover(preview, item, () => !file.files.length && !remove.checked);
          return;
        }
        try {
          preview.src = await readCover(file.files[0]);
          preview.hidden = false;
          remove.checked = false;
        } catch (error) {
          file.setCustomValidity(error.message);
          file.reportValidity();
        }
      };
      remove.onchange = () => {
        if (remove.checked) {
          file.value = '';
          file.setCustomValidity('');
          preview.removeAttribute('src');
          preview.hidden = true;
        } else showCover(preview, item, () => !file.files.length && !remove.checked);
      };
    }
    if (notices) {
      field(form, 'event_url', 'Link tham gia giao lưu online (tùy chọn)', {type: 'url', value: item.event_url, maxLength: 2083, wide: true});
    } else {
      if (shop) {
        const category = field(form, 'category', 'Danh mục', {value: item.category, maxLength: 120, required: true, wide: true});
        const choices = el('datalist');
        choices.id = 'categories-' + (item.id || 'new');
        for (const label of ['Tranh treo tường', 'Vật phẩm thật', 'Pháp Âm trạch']) {
          const option = el('option');
          option.value = label;
          choices.append(option);
        }
        category.setAttribute('list', choices.id);
        form.append(choices);
      }
      field(form, 'reward', 'Linh Thạch thưởng cho mỗi đơn được xác nhận', {type: 'number', value: item.reward ?? 0, min: 0, max: 1000000, required: true});
      field(form, 'price', 'Giá niêm yết (VNĐ)', {type: 'number', value: item.price, min: 0, max: 1e10, required: true});
      field(form, 'offer', 'Giá sau ưu đãi (VNĐ, có thể để trống)', {type: 'number', value: item.offer, min: 0, max: 1e10});
    }
    field(form, 'published', 'Hiển thị cho thành viên', {choices: {no: 'Bản nháp / Ẩn', yes: 'Đã đăng'}, value: item.published ? 'yes' : 'no'});
    wire(form, 'Lưu nội dung', async message => {
      const values = Object.fromEntries(new FormData(form));
      const payload = {
        title: values.title, body: values.body, category: values.category || '',
        reward: Number(values.reward || 0),
        price: Number(values.price || 0), offer: values.offer ? Number(values.offer) : null,
        event_url: values.event_url || null, published: values.published === 'yes', expected_revision: item.revision || 0,
      };
      if (payload.offer !== null && payload.offer > payload.price) {
        throw new Error('Giá sau ưu đãi phải nhỏ hơn hoặc bằng giá niêm yết.');
      }
      if (file?.files.length) payload.cover = await readCover(file.files[0]);
      else if (remove?.checked) payload.cover = null;
      if (!item.id) {
        onCreate(await api.post(endpoint, payload));
        form.reset();
        if (preview) {
          preview.removeAttribute('src');
          preview.hidden = true;
        }
      } else {
        item = await api.put(endpoint + '/' + item.id, payload);
        updateHeading();
        if (file) file.value = '';
        if (remove) remove.checked = false;
      }
      message.textContent = 'Đã lưu nội dung.';
    });
    editor.append(heading, form);
    return editor;
  }
  function registration(item, contact) {
    const editor = el('details');
    editor.append(el('summary', shop ? 'Đặt vật phẩm' : 'Đăng ký khóa học'));
    const form = el('form', undefined, 'course-form');
    field(form, 'full_name', 'Họ và tên', {required: true, maxLength: 160, autocomplete: 'name', value: contact.full_name});
    field(form, 'phone', 'Số điện thoại', {type: 'tel', required: true, maxLength: 24, autocomplete: 'tel', value: contact.phone});
    field(form, 'birth_date', 'Ngày tháng năm sinh (DD/MM/YYYY)', {
      required: true, maxLength: 10, placeholder: 'DD/MM/YYYY', pattern: '[0-9]{2}/[0-9]{2}/[0-9]{4}', autocomplete: 'bday',
    });
    field(form, 'address', 'Địa chỉ hiện tại', {required: true, maxLength: 500, autocomplete: 'street-address'});
    if (shop) field(form, 'quantity', 'Số lượng', {type: 'number', value: 1, min: 1, max: 100, required: true});
    field(form, 'note', 'Ghi chú', {multiline: true, maxLength: 2000, wide: true});
    const key = window.crypto?.randomUUID?.() || 'req_' + Date.now() + '_' + Math.random().toString(36).slice(2);
    wire(form, shop ? 'Gửi yêu cầu đặt hàng' : 'Gửi đăng ký', async message => {
      const values = Object.fromEntries(new FormData(form));
      const [day, month, year] = values.birth_date.split('/');
      const iso = [year, month, day].join('-');
      const date = new Date(iso + 'T00:00:00Z');
      const today = new Date();
      const localToday = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
      if (!Number.isFinite(date.getTime()) || date.toISOString().slice(0, 10) !== iso || iso < '1900-01-01' || iso > localToday) {
        throw new Error('Nhập ngày sinh hợp lệ theo định dạng DD/MM/YYYY.');
      }
      await api.post(endpoint + '/' + item.id + '/requests', {
        ...values, birth_date: iso, quantity: Number(values.quantity || 1), expected_revision: item.revision, request_key: key,
      });
      const result = el('p', 'Đã gửi. BTE sẽ liên hệ với anh/chị qua số điện thoại đã đăng ký.');
      result.setAttribute('role', 'status');
      editor.replaceWith(result);
    });
    editor.append(form);
    return editor;
  }
  async function showRequests(target, page) {
    target.setAttribute('aria-busy', 'true');
    try {
      const data = await api.get(endpoint + '/requests?page=' + page);
      target.replaceChildren();
      if (!data.items.length) target.append(el('p', 'Chưa có yêu cầu.'));
      for (const item of data.items) {
        const details = el('details');
        const heading = el('summary', item.title + ' · ' + item.full_name + ' · ' + statuses[item.status]);
        details.append(heading);
        const values = [
          ['Họ và tên', item.full_name], ['Số điện thoại', item.phone],
          ['Ngày sinh', formatDate(item.birth_date)], ['Địa chỉ hiện tại', item.address],
          ['Ghi chú', item.note || '—'], ['Ngày gửi', new Date(item.created_at).toLocaleString('vi-VN')],
          ['Linh Thạch thưởng theo đơn', item.reward ?? 0],
          ['Số lượng', item.quantity], ['Tổng theo giá lúc gửi', money.format(item.total)],
        ];
        const list = el('dl');
        for (const [label, value] of values) list.append(el('dt', label), el('dd', value, 'course-body'));
        const form = el('form', undefined, 'course-form');
        const select = field(form, 'status', 'Trạng thái xử lý', {choices: statuses, value: item.status});
        wire(form, 'Cập nhật trạng thái', async message => {
          const result = await api.api('PATCH', endpoint + '/requests/' + item.id, {status: select.value});
          heading.textContent = item.title + ' · ' + item.full_name + ' · ' + statuses[result.status];
          message.textContent = result.reward_granted ? 'Đã cộng ' + result.reward_granted + ' Linh Thạch vào tài khoản thành viên.' : 'Đã cập nhật trạng thái.';
        });
        details.append(list, form);
        target.append(details);
      }
      const nav = el('div', undefined, 'course-tabs');
      for (const [enabled, label, next] of [[page > 1, 'Trang trước', page - 1], [data.has_next, 'Trang sau', page + 1]]) {
        if (!enabled) continue;
        const button = el('button', label);
        button.onclick = () => showRequests(target, next);
        nav.append(button);
      }
      target.append(nav);
    } catch (error) {
      target.replaceChildren(el('p', error.message, 'course-error'));
    } finally {
      target.removeAttribute('aria-busy');
    }
  }
  async function load() {
    const {items, contact = {}} = await api.get(endpoint);
    state.textContent = '';
    if (admin) {
      const listings = el('section', undefined, 'course-card');
      listings.append(el('h2', 'Nội dung đăng trên trang thành viên'));
      const existing = el('div');
      listings.append(listingEditor({}, item => existing.prepend(listingEditor(item))), existing);
      for (const item of items) existing.append(listingEditor(item));
      host.append(listings);
      if (!notices) {
        const requests = el('section', undefined, 'course-card');
        requests.style.marginTop = '24px';
        const content = el('div', 'Đang tải…');
        const refresh = el('button', 'Tải lại danh sách');
        refresh.onclick = () => showRequests(content, 1);
        requests.append(el('h2', shop ? 'Yêu cầu đặt vật phẩm' : 'Danh sách đăng ký'), refresh, content);
        host.append(requests);
        await showRequests(content, 1);
      }
      return;
    }
    if (!items.length) {
      state.textContent = 'Hiện chưa có nội dung được đăng.';
      return;
    }
    if (!notices) host.className = 'course-grid';
    for (const item of items) {
      const card = el('article', undefined, 'course-card');
      const split = notices && item.has_cover;
      if (notices) card.classList.add('catalog-notice');
      if (split) card.classList.add('catalog-notice-with-cover');
      const content = split ? el('div') : card;
      if (split) card.append(content);
      if (item.has_cover) {
        const cover = el('img', undefined, 'catalog-cover');
        cover.alt = item.title;
        cover.hidden = true;
        card.append(cover);
        if ('IntersectionObserver' in window) {
          const observer = new IntersectionObserver(entries => {
            if (!entries[0].isIntersecting) return;
            observer.disconnect();
            showCover(cover, item);
          }, {rootMargin: '400px'});
          observer.observe(card);
        } else showCover(cover, item);
      }
      if (item.category) card.append(el('p', item.category, 'course-meta'));
      content.append(el('h2', item.title), el('p', item.body, 'course-body'));
      if (notices && item.event_url) {
        const link = el('a', 'Tham gia giao lưu online', 'course-action');
        link.href = item.event_url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        content.append(link);
      }
      if (!notices) {
        if (item.offer !== null) {
          const original = el('p', 'Giá niêm yết ');
          original.append(el('del', money.format(item.price)));
          card.append(original, el('p', 'Giá ưu đãi ' + money.format(item.offer), 'course-price'));
        } else {
          card.append(el('p', money.format(item.price), 'course-price'));
        }
        if (item.reward) card.append(el('p', 'Tặng ' + item.reward.toLocaleString('vi-VN') + ' Linh Thạch khi BTE xác nhận đơn', 'catalog-reward'));
        card.append(registration(item, contact));
      }
      host.append(card);
    }
  }
  load().catch(error => {
    state.classList.add('course-error');
    state.textContent = error.message;
  });
})();
