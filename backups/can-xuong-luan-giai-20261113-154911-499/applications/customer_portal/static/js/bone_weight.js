(function () {
  const form = document.getElementById('boneWeightForm');
  const result = document.getElementById('boneWeightResult');
  const state = document.getElementById('boneWeightState');
  const button = form.querySelector('button');
  const birthDate = form.elements.birth_date;

  function parseBirthDate(value) {
    const match = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(value.trim());
    if (!match) return null;
    const [, day, month, year] = match;
    if (Number(year) < 1900 || Number(year) > 2100) return null;
    const iso = year + '-' + month + '-' + day;
    const parsed = new Date(iso + 'T00:00:00Z');
    return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === iso ? iso : null;
  }

  function line(tag, value, css) {
    const element = document.createElement(tag);
    element.textContent = value;
    if (css) element.className = css;
    return element;
  }

  birthDate.addEventListener('input', () => birthDate.setCustomValidity(''));
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (button.disabled) return;
    const iso = parseBirthDate(birthDate.value);
    birthDate.setCustomValidity(iso ? '' : 'Nhập ngày hợp lệ theo DD/MM/YYYY, từ năm 1900 đến 2100.');
    if (!form.reportValidity()) return;

    const payload = Object.fromEntries(new FormData(form));
    payload.birth_date = iso;
    button.disabled = true;
    result.hidden = true;
    state.textContent = 'Đang tính…';
    try {
      const data = await BtePortal.post('/api/v1/can-xuong', payload);
      const labels = ['Năm', 'Tháng', 'Ngày', 'Giờ'];
      const breakdown = data.weights.map((value, index) => labels[index] + ' ' + value + ' chỉ');
      result.replaceChildren(
        line('h2', data.full_name + ' · ' + (data.gender === 'male' ? 'Nam' : 'Nữ')),
        line('p', data.birth_date + ' dương lịch · Giờ ' + data.hour_branch),
        line('p', 'Âm lịch ' + data.lunar_date + (data.lunar_leap ? ' (tháng nhuận)' : '') + ' · Năm ' + data.year_ganzhi),
        line('p', data.weight + ' · ' + data.classification, 'course-price'),
        line('p', breakdown.join(' + ')),
        line('h3', data.title),
        line('p', data.poem_label, 'course-meta'),
        line('blockquote', data.poem.join('\n'), 'course-body'),
        line('h3', 'Nghĩa bài thơ'),
        line('p', data.explanation),
        ...data.sections.flatMap(section => [line('h3', section.heading), line('p', section.text)])
      );
      result.hidden = false;
      state.textContent = 'Đã tính cân xương.';
    } catch (error) {
      state.textContent = error.message;
    } finally {
      button.disabled = false;
    }
  });
})();
