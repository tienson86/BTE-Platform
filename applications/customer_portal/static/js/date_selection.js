/**
 * Date Selection portal screens (lookup + personalized search).
 * Presentation only — classification comes from /api/v1/date-selection/*.
 */
(function (global) {
  var BRANCHES = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"];
  var HOUR_WINDOWS = [
    { branch: "Tý", start: 23 * 60 + 1, end: 1 * 60, cross: true },
    { branch: "Sửu", start: 1 * 60 + 1, end: 3 * 60 },
    { branch: "Dần", start: 3 * 60 + 1, end: 5 * 60 },
    { branch: "Mão", start: 5 * 60 + 1, end: 7 * 60 },
    { branch: "Thìn", start: 7 * 60 + 1, end: 9 * 60 },
    { branch: "Tỵ", start: 9 * 60 + 1, end: 11 * 60 },
    { branch: "Ngọ", start: 11 * 60 + 1, end: 13 * 60 },
    { branch: "Mùi", start: 13 * 60 + 1, end: 15 * 60 },
    { branch: "Thân", start: 15 * 60 + 1, end: 17 * 60 },
    { branch: "Dậu", start: 17 * 60 + 1, end: 19 * 60 },
    { branch: "Tuất", start: 19 * 60 + 1, end: 21 * 60 },
    { branch: "Hợi", start: 21 * 60 + 1, end: 23 * 60 },
  ];

  function t(key) {
    var value = global.BteI18n ? BteI18n.t(key) : key;
    if (value && value !== key) return value;
    return LABELS[key] || key;
  }

  var LABELS = {
    "date_selection.solar_date": "Ngày dương",
    "date_selection.lunar_date": "Ngày âm",
    "date_selection.year_ganzhi": "Can Chi năm",
    "date_selection.month_ganzhi": "Can Chi tháng",
    "date_selection.day_ganzhi": "Can Chi ngày",
    "date_selection.day_result": "Kết quả ngày",
    "date_selection.hour_result": "Kết quả giờ",
    "date_selection.cung_phi": "Cung Phi",
    "date_selection.nayin": "Nạp âm",
    "date_selection.hanh_cung": "Hành Cung",
    "date_selection.trach_group": "Nhóm Trạch",
    "date_selection.clock": "Đồng hồ",
    "date_selection.hour_branch": "Giờ",
    "date_selection.hour_window": "Khung giờ",
    "date_selection.current_hour": "Giờ hiện hành",
    "date_selection.hour_ganzhi": "Can Chi giờ",
    "date_selection.current_ke": "Khắc hiện hành",
    "date_selection.hour_select": "Chọn giờ",
    "date_selection.ke_panel": "Sáu khắc",
    "date_selection.ke_label": "Khắc",
    "date_selection.weekdays": "T2,T3,T4,T5,T6,T7,CN",
  };

  function apiPost(path, body) {
    if (!global.BtePortal || typeof global.BtePortal.post !== "function") {
      throw new Error("BtePortal is not loaded");
    }
    return global.BtePortal.post(path, body);
  }

  function weekdayLabels() {
    return t("date_selection.weekdays").split(",");
  }

  function branchFromClock(now) {
    var minutes = now.getHours() * 60 + now.getMinutes();
    for (var i = 0; i < HOUR_WINDOWS.length; i += 1) {
      var win = HOUR_WINDOWS[i];
      if (win.cross) {
        if (minutes >= win.start || minutes <= win.end) return win.branch;
      } else if (minutes >= win.start && minutes <= win.end) {
        return win.branch;
      }
    }
    return "Tý";
  }

  function keIndexFromClock(now, hourPayload) {
    var window = hourPayload && hourPayload.window;
    if (!window) return 1;
    var clock = now.getHours() * 60 + now.getMinutes();
    var start = window.start_hour * 60 + window.start_minute;
    var elapsed = window.is_cross_day && clock < start ? 24 * 60 - start + clock : clock - start;
    var index = Math.floor(elapsed / 20) + 1;
    if (index < 1) return 1;
    if (index > 6) return 6;
    return index;
  }

  var ELEMENT_TOKEN = { "Mộc": "moc", "Hỏa": "hoa", "Thổ": "tho", "Kim": "kim", "Thủy": "thuy" };
  var POSITIVE_KE = { dai_an: true, tieu_cat: true, toc_hy: true };

  function kv(dl, rows) {
    dl.innerHTML = rows
      .map(function (row) {
        return "<dt>" + row[0] + "</dt><dd>" + row[1] + "</dd>";
      })
      .join("");
  }

  function elementBadge(label) {
    if (!label) return "—";
    var token = ELEMENT_TOKEN[label] || "kim";
    return '<span class="ds-badge ds-badge--' + token + '">' + label + "</span>";
  }

  function cungBadge(label) {
    if (!label) return "—";
    return '<span class="ds-badge ds-badge--cung">' + label + "</span>";
  }

  function identityOf(entity) {
    var trach = entity.trach || {};
    return {
      ganzhi: entity.ganzhi || (entity.calendar && entity.calendar.day_ganzhi) || "",
      nayin: entity.nayin || entity.nayin_element || "",
      cung: entity.cung || trach.cung || "",
      hanhCung: entity.cung_element || trach.element_label || "",
      trachLabel: entity.trach_group_label || trach.trach_group_label || "",
    };
  }

  function fillDetail(dl, day) {
    var cal = day.calendar;
    var identity = identityOf(day);
    kv(dl, [
      [t("date_selection.solar_date"), cal.solar_label],
      [t("date_selection.lunar_date"), cal.lunar_label],
      [t("date_selection.year_ganzhi"), cal.year_ganzhi],
      [t("date_selection.month_ganzhi"), cal.month_ganzhi || day.month_ganzhi || "—"],
      [t("date_selection.day_ganzhi"), cal.day_ganzhi],
      [t("date_selection.day_result"), day.six_state.label],
      [t("date_selection.nayin"), elementBadge(identity.nayin)],
      [t("date_selection.cung_phi"), cungBadge(identity.cung)],
      [t("date_selection.hanh_cung"), elementBadge(identity.hanhCung)],
      [t("date_selection.trach_group"), identity.trachLabel || "—"],
    ]);
  }

  function fillHour(dl, hour) {
    var identity = identityOf(hour);
    kv(dl, [
      [t("date_selection.hour_branch"), hour.window.branch],
      [t("date_selection.hour_window"), hour.window.time_range],
      [t("date_selection.hour_ganzhi"), hour.ganzhi],
      [t("date_selection.hour_result"), hour.six_state.label],
      [t("date_selection.nayin"), elementBadge(identity.nayin)],
      [t("date_selection.cung_phi"), cungBadge(identity.cung)],
      [t("date_selection.hanh_cung"), elementBadge(identity.hanhCung)],
      [t("date_selection.trach_group"), identity.trachLabel || "—"],
    ]);
  }

  function fillKe(container, hour, currentIndex) {
    container.innerHTML = hour.ke_slots
      .map(function (slot) {
        var current = slot.ke_index === currentIndex;
        var tone = !current && POSITIVE_KE[slot.six_state.code] ? ' data-tone="positive"' : "";
        var currentAttr = current ? ' data-current="true"' : "";
        return (
          '<div class="ds-ke-row"' +
          currentAttr +
          tone +
          '><span class="ds-ke-row__time">' +
          slot.time_range +
          '</span><span class="ds-ke-row__label">' +
          t("date_selection.ke_label") +
          " " +
          slot.ke_index +
          '</span><span class="ds-ke-row__result">' +
          slot.six_state.label +
          "</span></div>"
        );
      })
      .join("");
  }

  function tickClock() {
    var now = new Date();
    var hourEl = document.getElementById("dsHandHour");
    var minuteEl = document.getElementById("dsHandMinute");
    var secondEl = document.getElementById("dsHandSecond");
    if (!hourEl) return now;
    var h = now.getHours() % 12;
    var m = now.getMinutes();
    var s = now.getSeconds();
    hourEl.style.transform = "rotate(" + (h * 30 + m * 0.5) + "deg)";
    minuteEl.style.transform = "rotate(" + m * 6 + "deg)";
    secondEl.style.transform = "rotate(" + s * 6 + "deg)";
    return now;
  }

  function LookupController() {
    this.year = new Date().getFullYear();
    this.month = new Date().getMonth() + 1;
    this.selectedDay = new Date().getDate();
    this.monthData = null;
    this.dayData = null;
    this.selectedBranch = null;
    this.manualHour = false;
  }

  LookupController.prototype.init = function () {
    var self = this;
    var select = document.getElementById("dsHourSelect");
    BRANCHES.forEach(function (branch) {
      var option = document.createElement("option");
      option.value = branch;
      option.textContent = branch;
      select.appendChild(option);
    });
    document.getElementById("dsPrev").addEventListener("click", function () {
      self.month -= 1;
      if (self.month < 1) {
        self.month = 12;
        self.year -= 1;
      }
      self.selectedDay = 1;
      self.loadMonth();
    });
    document.getElementById("dsNext").addEventListener("click", function () {
      self.month += 1;
      if (self.month > 12) {
        self.month = 1;
        self.year += 1;
      }
      self.selectedDay = 1;
      self.loadMonth();
    });
    select.addEventListener("change", function () {
      self.manualHour = true;
      self.selectedBranch = select.value;
      self.renderHour();
    });
    var weekdays = document.getElementById("dsWeekdays");
    weekdays.innerHTML = weekdayLabels()
      .map(function (label) {
        return '<div class="ds-calendar__head">' + label + "</div>";
      })
      .join("");
    this.loadMonth();
    this.tick();
    setInterval(function () {
      self.tick();
    }, 1000);
  };

  LookupController.prototype.loadMonth = function () {
    var self = this;
    document.getElementById("dsCalTitle").textContent =
      "Tháng " + this.month + "/" + this.year;
    return apiPost("/api/v1/date-selection/month", { year: this.year, month: this.month })
      .then(function (res) {
        self.monthData = res.data;
        self.renderMonth();
        return self.loadDay(self.selectedDay);
      })
      .catch(function (err) {
        if (global.BteShell) BteShell.toast(err.message || "Lỗi", "error");
      });
  };

  LookupController.prototype.renderMonth = function () {
    var self = this;
    var root = document.getElementById("dsCalendar");
    var cells = this.monthData.cells;
    var firstWeekday = cells[0].weekday;
    var html = "";
    for (var i = 0; i < firstWeekday; i += 1) {
      html += '<div class="ds-day" hidden></div>';
    }
    cells.forEach(function (cell) {
      var lunar = cell.lunar_day + "/" + cell.lunar_month;
      var selected = cell.solar_day === self.selectedDay ? ' data-selected="true"' : "";
      html +=
        '<button type="button" class="ds-day"' +
        selected +
        ' data-day="' +
        cell.solar_day +
        '"><span class="ds-day__solar">' +
        cell.solar_day +
        '</span><span class="ds-day__lunar">' +
        lunar +
        '</span><span class="ds-day__state">' +
        cell.six_state.label +
        "</span></button>";
    });
    root.innerHTML = html;
    root.querySelectorAll("[data-day]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        self.selectedDay = Number(btn.getAttribute("data-day"));
        self.renderMonth();
        self.loadDay(self.selectedDay);
      });
    });
  };

  LookupController.prototype.loadDay = function (day) {
    var self = this;
    return apiPost("/api/v1/date-selection/day", {
        year: this.year,
        month: this.month,
        day: day,
      })
      .then(function (res) {
        self.dayData = res.data;
        fillDetail(document.getElementById("dsDetail"), self.dayData);
        if (!self.manualHour) {
          self.selectedBranch = branchFromClock(new Date());
          document.getElementById("dsHourSelect").value = self.selectedBranch;
        }
        self.renderHour();
        self.renderLiveHour(new Date());
      });
  };

  LookupController.prototype.findHour = function (branch) {
    if (!this.dayData) return null;
    for (var i = 0; i < this.dayData.hours.length; i += 1) {
      if (this.dayData.hours[i].window.branch === branch) return this.dayData.hours[i];
    }
    return this.dayData.hours[0];
  };

  LookupController.prototype.renderHour = function () {
    var hour = this.findHour(this.selectedBranch);
    if (!hour) return;
    fillHour(document.getElementById("dsHourDetail"), hour);
    fillKe(document.getElementById("dsKeList"), hour, 0);
  };

  LookupController.prototype.renderLiveHour = function (now) {
    if (!this.dayData) return;
    var live = this.findHour(branchFromClock(now));
    if (!live) return;
    var keIndex = keIndexFromClock(now, live);
    var ke = live.ke_slots[keIndex - 1];
    kv(document.getElementById("dsLiveHour"), [
      [t("date_selection.current_hour"), live.window.branch],
      [t("date_selection.hour_window"), live.window.time_range],
      [t("date_selection.hour_ganzhi"), live.ganzhi],
      [t("date_selection.hour_result"), live.six_state.label],
      [t("date_selection.current_ke"), ke ? ke.six_state.label + " · " + ke.time_range : ""],
    ]);
    if (!this.manualHour) {
      fillKe(document.getElementById("dsKeList"), live, keIndex);
    }
  };

  LookupController.prototype.tick = function () {
    var now = tickClock();
    this.renderLiveHour(now);
  };

  function SearchController() {
    this.form = document.getElementById("dsSearchForm");
  }

  SearchController.prototype.init = function () {
    var self = this;
    var now = new Date();
    var monthInput = document.getElementById("dsTargetMonth");
    monthInput.value =
      now.getFullYear() + "-" + String(now.getMonth() + 1).padStart(2, "0");
    this.form.addEventListener("submit", function (event) {
      event.preventDefault();
      self.submit();
    });
  };

  SearchController.prototype.showError = function (id, message) {
    var el = document.getElementById(id);
    if (!el) return false;
    if (!message) {
      el.hidden = true;
      el.textContent = "";
      return false;
    }
    el.hidden = false;
    el.textContent = message;
    return true;
  };

  SearchController.prototype.submit = function () {
    var name = document.getElementById("dsFullName").value.trim();
    var gender = document.getElementById("dsGender").value;
    var birth = document.getElementById("dsBirth").value;
    var target = document.getElementById("dsTargetMonth").value;
    var ok = true;
    if (!name) ok = !this.showError("err_full_name", t("date_selection.name_required")) && ok;
    else this.showError("err_full_name", "");
    if (!gender) ok = !this.showError("err_gender", t("date_selection.gender_required")) && ok;
    else this.showError("err_gender", "");
    if (!birth) ok = !this.showError("err_birth", t("date_selection.birth_required")) && ok;
    else this.showError("err_birth", "");
    if (!ok) return;
    var birthParts = birth.split("-");
    var targetParts = (target || "").split("-");
    var payload = {
      full_name: name,
      gender: gender,
      birth_year: Number(birthParts[0]),
      birth_month: Number(birthParts[1]),
      birth_day: Number(birthParts[2]),
      target_year: Number(targetParts[0]) || new Date().getFullYear(),
      target_month: Number(targetParts[1]) || new Date().getMonth() + 1,
    };
    var self = this;
    apiPost("/api/v1/date-selection/search", payload)
      .then(function (res) {
        self.render(res.data);
      })
      .catch(function (err) {
        if (global.BteShell) BteShell.toast(err.message || "Lỗi", "error");
      });
  };

  SearchController.prototype.render = function (data) {
    var person = data.person;
    var block = document.getElementById("dsPerson");
    block.hidden = false;
    kv(document.getElementById("dsPersonDl"), [
      [t("date_selection.full_name"), person.full_name],
      [t("date_selection.gender"), person.gender_label],
      [t("date_selection.birth_solar"), person.solar_label],
      [t("date_selection.lunar_date"), person.lunar_label],
      ["Can Chi", person.ganzhi],
      [t("date_selection.cung_phi"), person.trach.cung],
      [t("date_selection.element"), person.trach.element_label],
      [t("date_selection.trach_group"), person.trach.trach_group_label],
    ]);
    var root = document.getElementById("dsResults");
    if (!data.dates.length) {
      root.innerHTML = '<p class="muted">' + t("date_selection.no_results") + "</p>";
      return;
    }
    root.innerHTML = data.dates
      .map(function (item) {
        var cal = item.day.calendar;
        var trach = item.day.trach;
        var primary = item.recommendations[0];
        var others = item.recommendations.slice(1);
        return (
          '<article class="bte-card ds-result"><div class="ds-card-date">' +
          cal.solar_label +
          '</div><div class="ds-card-lunar">' +
          cal.lunar_label +
          ' âm</div><div class="ds-card-state">' +
          item.day.six_state.label +
          "</div><div>" +
          trach.cung +
          " · " +
          trach.element_label +
          " · " +
          trach.trach_group_label +
          "</div><div><strong>" +
          t("date_selection.recommended_hours") +
          "</strong></div><div class='ds-hours'>" +
          (primary ? primary.time_range : "") +
          (others.length
            ? "<div>" +
              t("date_selection.other_hours") +
              ": " +
              others
                .map(function (row) {
                  return row.time_range;
                })
                .join(", ") +
              "</div>"
            : "") +
          "</div></article>"
        );
      })
      .join("");
  };

  function boot() {
    var page = document.querySelector(".ds-page");
    if (!page) return;
    var screen = page.getAttribute("data-screen");
    if (screen === "lookup") new LookupController().init();
    if (screen === "search") new SearchController().init();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  global.BteDateSelection = {
    branchFromClock: branchFromClock,
    BRANCHES: BRANCHES,
  };
})(typeof window !== "undefined" ? window : globalThis);
