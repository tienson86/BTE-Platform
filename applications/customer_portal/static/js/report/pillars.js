/**
 * Tier 2 — Four Pillars Workspace (Blueprint V1.1).
 * Presentation only. Does not invent BaZi facts.
 */
(function (global) {
  var MISSING = "--";

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function unavailable(value) {
    return (
      value === null ||
      value === undefined ||
      value === "" ||
      value === MISSING
    );
  }

  function displayOrUnavailable(value) {
    return unavailable(value) ? t("report.unavailable") : String(value);
  }

  function StemBadge(stem, isDay) {
    var missing = unavailable(stem);
    return (
      '<div class="fp-stem' +
      (isDay ? " fp-stem-day" : "") +
      (missing ? " fp-slot-miss" : "") +
      '" data-component="StemBadge" title="' +
      esc(t("bazi.stem") + ": " + displayOrUnavailable(stem)) +
      '">' +
      '<span class="fp-field-label">' +
      esc(t("bazi.stem")) +
      "</span>" +
      '<span class="fp-stem-value" aria-label="' +
      esc(t("bazi.stem")) +
      '">' +
      esc(displayOrUnavailable(stem)) +
      "</span></div>"
    );
  }

  function BranchBadge(branch, isDay) {
    var missing = unavailable(branch);
    return (
      '<div class="fp-branch' +
      (isDay ? " fp-branch-day" : "") +
      (missing ? " fp-slot-miss" : "") +
      '" data-component="BranchBadge" title="' +
      esc(t("bazi.branch") + ": " + displayOrUnavailable(branch)) +
      '">' +
      '<span class="fp-field-label">' +
      esc(t("bazi.branch")) +
      "</span>" +
      '<span class="fp-branch-value" aria-label="' +
      esc(t("bazi.branch")) +
      '">' +
      esc(displayOrUnavailable(branch)) +
      "</span></div>"
    );
  }

  function HiddenStemGroup(list) {
    var items = Array.isArray(list) ? list : [];
    if (!items.length) {
      return (
        '<div class="fp-hidden" data-component="HiddenStemGroup">' +
        '<span class="fp-field-label">' +
        esc(t("bazi.hidden")) +
        '</span><span class="fp-chip fp-chip-miss">' +
        esc(t("report.unavailable")) +
        "</span></div>"
      );
    }
    return (
      '<div class="fp-hidden" data-component="HiddenStemGroup">' +
      '<span class="fp-field-label">' +
      esc(t("bazi.hidden")) +
      '</span><div class="fp-chip-row" role="list">' +
      items
        .map(function (stem) {
          return (
            '<span class="fp-chip" role="listitem" title="' +
            esc(t("bazi.hidden") + ": " + stem) +
            '">' +
            esc(stem) +
            "</span>"
          );
        })
        .join("") +
      "</div></div>"
    );
  }

  function TenGodBadge(list) {
    var items = Array.isArray(list) ? list : [];
    if (!items.length) {
      return (
        '<div class="fp-tengod" data-component="TenGodBadge">' +
        '<span class="fp-field-label">' +
        esc(t("bazi.ten_god")) +
        '</span><span class="fp-badge fp-badge-miss">' +
        esc(t("report.unavailable")) +
        "</span></div>"
      );
    }
    return (
      '<div class="fp-tengod" data-component="TenGodBadge">' +
      '<span class="fp-field-label">' +
      esc(t("bazi.ten_god")) +
      '</span><div class="fp-badge-row">' +
      items
        .map(function (god) {
          return (
            '<span class="fp-badge" title="' +
            esc(t("bazi.ten_god") + ": " + god) +
            '">' +
            esc(god) +
            "</span>"
          );
        })
        .join("") +
      "</div></div>"
    );
  }

  function NaYinLabel(napAm) {
    return (
      '<div class="fp-nayin" data-component="NaYinLabel">' +
      '<span class="fp-meta-k">' +
      esc(t("bazi.nap_am")) +
      '</span><span class="fp-meta-v' +
      (unavailable(napAm) ? " fp-slot-miss" : "") +
      '">' +
      esc(displayOrUnavailable(napAm)) +
      "</span></div>"
    );
  }

  function LifeStageLabel(changSheng) {
    return (
      '<div class="fp-lifestage" data-component="LifeStageLabel">' +
      '<span class="fp-meta-k">' +
      esc(t("bazi.chang_sheng")) +
      '</span><span class="fp-status' +
      (unavailable(changSheng) ? " fp-slot-miss" : "") +
      '">' +
      esc(displayOrUnavailable(changSheng)) +
      "</span></div>"
    );
  }

  function DayMasterRelation(col) {
    var isDay = !!col.isDay;
    var value = col.relation_to_day_master;
    var label = isDay
      ? t("bazi.role_day_master")
      : t("bazi.relation_to_day_master");
    return (
      '<div class="fp-relation' +
      (isDay ? " fp-relation-day" : "") +
      '" data-component="DayMasterRelation">' +
      '<span class="fp-field-label">' +
      esc(label) +
      '</span><span class="fp-relation-value' +
      (unavailable(value) ? " fp-slot-miss" : "") +
      '" title="' +
      esc(label + ": " + displayOrUnavailable(value)) +
      '">' +
      esc(displayOrUnavailable(value)) +
      "</span></div>"
    );
  }

  function PillarColumn(col) {
    var isDay = !!col.isDay;
    var roleLabel = col.label || t("bazi.pillar_" + (col.role_key || "day"));
    var hiddenList =
      col.hidden_list && col.hidden_list.length
        ? col.hidden_list
        : unavailable(col.hidden)
          ? []
          : String(col.hidden)
              .split(/[,;/|、]+/)
              .map(function (s) {
                return s.trim();
              })
              .filter(Boolean);
    var tenList =
      col.ten_god_list && col.ten_god_list.length
        ? col.ten_god_list
        : unavailable(col.ten_god)
          ? []
          : [String(col.ten_god)];

    return (
      '<article class="fp-col' +
      (isDay ? " fp-col-day rpt-accent-day" : "") +
      '" data-component="PillarColumn" data-pillar="' +
      esc(col.id || "") +
      '" tabindex="0" aria-label="' +
      esc(roleLabel + (isDay ? " — " + t("bazi.day_master") : "")) +
      '">' +
      '<header class="fp-col-head">' +
      '<span class="fp-role">' +
      esc(roleLabel) +
      "</span>" +
      (isDay
        ? '<span class="fp-day-tag">' + esc(t("bazi.day_master")) + "</span>"
        : "") +
      "</header>" +
      '<div class="fp-identity">' +
      StemBadge(col.stem, isDay) +
      BranchBadge(col.branch, isDay) +
      "</div>" +
      HiddenStemGroup(hiddenList) +
      TenGodBadge(tenList) +
      DayMasterRelation(col) +
      '<details class="fp-meta" data-fp-meta open>' +
      "<summary>" +
      esc(t("bazi.pillar_meta")) +
      "</summary>" +
      '<div class="fp-meta-body">' +
      LifeStageLabel(col.chang_sheng) +
      NaYinLabel(col.nap_am) +
      "</div></details></article>"
    );
  }

  function FourPillarsWorkspace(columns) {
    var cols = Array.isArray(columns) ? columns : [];
    if (!cols.length) {
      return (
        '<div class="fp-workspace" data-component="FourPillarsWorkspace">' +
        '<p class="rpt-caption">' +
        esc(t("report.unavailable")) +
        "</p></div>"
      );
    }
    return (
      '<div class="fp-workspace" data-component="FourPillarsWorkspace" role="group" aria-label="' +
      esc(t("report.tier.bazi")) +
      '">' +
      '<p class="fp-workspace-hint rpt-caption">' +
      esc(t("bazi.workspace_hint")) +
      "</p>" +
      '<div class="fp-grid">' +
      cols.map(PillarColumn).join("") +
      "</div></div>"
    );
  }

  function bind(root) {
    if (!root) return;
    root.querySelectorAll(".fp-col").forEach(function (col) {
      if (col.__fpBound) return;
      col.__fpBound = true;
      col.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") {
          var meta = col.querySelector("details[data-fp-meta]");
          if (!meta) return;
          if (ev.target && ev.target.closest && ev.target.closest("details")) {
            return;
          }
          ev.preventDefault();
          meta.open = !meta.open;
        }
      });
    });
  }

  global.BtePillars = {
    render: FourPillarsWorkspace,
    bind: bind,
    components: {
      FourPillarsWorkspace: FourPillarsWorkspace,
      PillarColumn: PillarColumn,
      StemBadge: StemBadge,
      BranchBadge: BranchBadge,
      HiddenStemGroup: HiddenStemGroup,
      TenGodBadge: TenGodBadge,
      NaYinLabel: NaYinLabel,
      LifeStageLabel: LifeStageLabel,
      DayMasterRelation: DayMasterRelation,
    },
  };
})(typeof window !== "undefined" ? window : globalThis);
