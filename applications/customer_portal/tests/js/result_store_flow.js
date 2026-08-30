/**
 * Node harness for BtePortal.ResultStore.
 *
 * Loads the browser module in a sandbox with in-memory Web Storage and walks
 * the Analyze -> Result -> Dashboard -> History -> Reports -> Result flow,
 * asserting that last_result never changes outside of an Analyze run.
 *
 * Prints one "PASS <name>" / "FAIL <name>: <detail>" line per check and exits
 * with 1 when any check fails. Driven by test_result_store.py.
 */
import fs from "fs";
import path from "path";
import vm from "vm";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const MODULE_PATH = path.resolve(
  __dirname,
  "..",
  "..",
  "static",
  "js",
  "result_store.js"
);

class MemoryStorage {
  constructor() {
    this.map = new Map();
  }
  getItem(key) {
    return this.map.has(key) ? this.map.get(key) : null;
  }
  setItem(key, value) {
    this.map.set(String(key), String(value));
  }
  removeItem(key) {
    this.map.delete(key);
  }
  keys() {
    return Array.from(this.map.keys()).sort();
  }
}

function newStore() {
  const sandbox = {
    sessionStorage: new MemoryStorage(),
    localStorage: new MemoryStorage(),
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(fs.readFileSync(MODULE_PATH, "utf8"), sandbox, {
    filename: MODULE_PATH,
  });
  return {
    store: sandbox.BtePortal.ResultStore,
    session: sandbox.sessionStorage,
    local: sandbox.localStorage,
  };
}

const results = [];

function check(name, condition, detail) {
  results.push({ name: name, ok: Boolean(condition), detail: detail || "" });
}

function sameJson(a, b) {
  return JSON.stringify(a) === JSON.stringify(b);
}

function result(tag) {
  return {
    input: { year: 1987, month: 1, day: 21, tag: tag },
    data: { calendar: { solar_date: "21/01/1987", lunar_date: "22/12/" + tag, calendar_rule_version: "G1-10C" } },
  };
}

function testKeysAreSeparate() {
  const ctx = newStore();
  check("keys.last_is_bte_last_result", ctx.store.LAST_KEY === "bte_last_result", ctx.store.LAST_KEY);
  check("keys.history_is_bte_history", ctx.store.HISTORY_KEY === "bte_history", ctx.store.HISTORY_KEY);
  check(
    "keys.last_and_history_differ",
    ctx.store.LAST_KEY !== ctx.store.HISTORY_KEY,
    ctx.store.LAST_KEY
  );

  ctx.store.save(result("A"));
  check(
    "keys.last_holds_single_result",
    sameJson(JSON.parse(ctx.session.getItem("bte_last_result")), result("A")),
    ctx.session.getItem("bte_last_result")
  );
  check(
    "keys.history_holds_a_list",
    Array.isArray(JSON.parse(ctx.session.getItem("bte_history"))),
    ctx.session.getItem("bte_history")
  );
}

function testFullFlowKeepsLastResult() {
  const ctx = newStore();
  const store = ctx.store;

  const older = result("OLD");
  store.saveHistory(older);
  check("flow.history_only_does_not_create_last", store.load() === null, JSON.stringify(store.load()));
  check("flow.history_appended", store.loadHistory().length === 1, String(store.loadHistory().length));

  // Analyze
  const analyzed = result("A");
  check("flow.analyze_saved", store.save(analyzed) === true, "");
  check("flow.analyze_is_last", sameJson(store.load(), analyzed), JSON.stringify(store.load()));
  check("flow.analyze_appended_history", store.loadHistory().length === 2, String(store.loadHistory().length));

  // Result
  check("flow.result_renders_analyze", sameJson(store.loadForView(), analyzed), JSON.stringify(store.loadForView()));

  // Dashboard recent -> open an older chart
  store.selectForView(older);
  check("flow.dashboard_keeps_last", sameJson(store.load(), analyzed), JSON.stringify(store.load()));
  check("flow.dashboard_view_is_older", sameJson(store.loadForView(), older), JSON.stringify(store.loadForView()));

  // History -> append another entry
  store.saveHistory(result("H"));
  check("flow.history_keeps_last", sameJson(store.load(), analyzed), JSON.stringify(store.load()));
  check("flow.history_appended_again", store.loadHistory().length === 3, String(store.loadHistory().length));

  // Reports -> open report
  store.selectForView(older);
  check("flow.reports_keeps_last", sameJson(store.load(), analyzed), JSON.stringify(store.load()));

  // Back on Result
  check("flow.result_renders_selection", sameJson(store.loadForView(), older), JSON.stringify(store.loadForView()));
  check("flow.last_result_untouched", sameJson(store.load(), analyzed), JSON.stringify(store.load()));

  // A new Analyze wins over the selection
  const reanalyzed = result("B");
  store.save(reanalyzed);
  check("flow.new_analyze_is_last", sameJson(store.load(), reanalyzed), JSON.stringify(store.load()));
  check("flow.new_analyze_clears_view", sameJson(store.loadForView(), reanalyzed), JSON.stringify(store.loadForView()));
}

function testSelectForViewNeverWritesLastKey() {
  const ctx = newStore();
  ctx.store.selectForView(result("X"));
  check("view.no_last_key_written", ctx.session.getItem("bte_last_result") === null, ctx.session.getItem("bte_last_result"));
  check("view.no_local_copy", ctx.local.getItem("bte_view_result") === null, ctx.local.getItem("bte_view_result"));
  check("view.no_legacy_key_written", ctx.session.getItem("bte_portal_last_result") === null, "");
}

function testClearAndHistoryIsolation() {
  const ctx = newStore();
  const store = ctx.store;
  store.save(result("A"));
  store.clear();
  check("clear.last_removed", store.load() === null, JSON.stringify(store.load()));
  check("clear.history_survives", store.loadHistory().length === 1, String(store.loadHistory().length));

  store.save(result("A"));
  store.clearHistory();
  check("clear.history_removed", store.loadHistory().length === 0, String(store.loadHistory().length));
  check("clear.last_survives_history_clear", sameJson(store.load(), result("A")), JSON.stringify(store.load()));
  check(
    "clear.history_removed_from_local",
    ctx.local.getItem("bte_history") === null,
    ctx.local.getItem("bte_history")
  );
}

function testLegacyKeysStillReadable() {
  const ctx = newStore();
  ctx.local.setItem("bte_portal_last_result", JSON.stringify(result("LEGACY")));
  ctx.local.setItem("bte_portal_history", JSON.stringify([{ id: "legacy-1", saved_at: "2026-01-01" }]));
  check("legacy.last_readable", sameJson(ctx.store.load(), result("LEGACY")), JSON.stringify(ctx.store.load()));
  check("legacy.history_readable", ctx.store.loadHistory().length === 1, String(ctx.store.loadHistory().length));
  ctx.store.clear();
  check("legacy.clear_removes_legacy_last", ctx.store.load() === null, JSON.stringify(ctx.store.load()));
}

function testRejectsInvalidPayload() {
  const ctx = newStore();
  check("guard.save_rejects_null", ctx.store.save(null) === false, "");
  check("guard.save_rejects_without_data", ctx.store.save({ input: {} }) === false, "");
  check("guard.view_rejects_without_data", ctx.store.selectForView({ input: {} }) === false, "");
  check("guard.nothing_persisted", ctx.session.keys().length === 0, ctx.session.keys().join(","));
}

function testCurrentResultPrecedence() {
  const ctx = newStore();
  const store = ctx.store;
  const stale = result("OLD");
  const fresh = result("FRESH");
  store.save(stale);
  store.save(fresh);
  store.selectForView(stale);

  check("current.load_is_fresh", sameJson(store.load(), fresh), JSON.stringify(store.load()));
  check(
    "current.loadCurrent_is_fresh",
    store.loadCurrent().data.calendar.lunar_date.indexOf("FRESH") !== -1,
    JSON.stringify(store.loadCurrent())
  );
  check(
    "current.default_display_is_fresh",
    store.resolveForDisplay(false).data.calendar.lunar_date.indexOf("FRESH") !== -1,
    JSON.stringify(store.resolveForDisplay(false))
  );
  check(
    "current.history_without_id_stays_fresh",
    store.resolveForDisplay(true).data.calendar.lunar_date.indexOf("FRESH") !== -1,
    JSON.stringify(store.resolveForDisplay(true))
  );
  const viewId = JSON.parse(ctx.session.getItem("bte_view_analysis_id"));
  check(
    "current.history_display_is_stale",
    store.resolveForDisplay(true, viewId).data.calendar.lunar_date.indexOf("OLD") !== -1,
    JSON.stringify(store.resolveForDisplay(true, viewId))
  );
  check(
    "current.analysis_id_present",
    typeof store.getCurrentAnalysisId() === "string" && store.getCurrentAnalysisId().length > 0,
    String(store.getCurrentAnalysisId())
  );
  check(
    "current.loadForView_still_supports_history",
    sameJson(store.loadForView(), stale),
    JSON.stringify(store.loadForView())
  );
}

function testG205HistorySnapshotPolicy() {
  const ctx = newStore();
  const store = ctx.store;
  const first = {
    analysis_id: "id-a",
    input: { year: 1985, month: 9, day: 18, hour: 8, minute: 0, full_name: "Ngô Đắc Dũng" },
    data: {
      analysis_id: "id-a",
      request_id: "id-a",
      result_meta: {
        created_at: "2026-08-21T01:00:00.000Z",
        customer_contract: "analysis_result.UsefulGodView@1.5",
        release_label: "BTE V1.0 — Gate 1 Core Engine",
      },
      useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
      calendar: { lunar_date: "DUNG", calendar_rule_version: "G1-10C" },
      useful_god: { useful_display: "Thủy · Nhâm · Thực Thần" },
    },
  };
  store.save(first);
  store.save(first);
  store.save(first);
  check("g205.save_once", store.loadHistory().length === 1, String(store.loadHistory().length));
  const currentId = store.getCurrentAnalysisId();
  check("g205.current_id_stable", currentId === "id-a", String(currentId));

  const second = {
    analysis_id: "id-b",
    input: { year: 1984, month: 7, day: 13, hour: 21, minute: 1, full_name: "Vũ Thị Thanh Tuyền" },
    data: {
      analysis_id: "id-b",
      request_id: "id-b",
      result_meta: { created_at: "2026-08-21T02:00:00.000Z", customer_contract: "analysis_result.UsefulGodView@1.5" },
      useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
      calendar: { lunar_date: "TUYEN", calendar_rule_version: "G1-10C" },
      useful_god: { useful_display: "Mộc · Ất · Chính Quan" },
    },
  };
  store.save(second);
  check("g205.two_analyzes_two_rows", store.loadHistory().length === 2, String(store.loadHistory().length));
  check("g205.current_is_b", store.getCurrentAnalysisId() === "id-b", String(store.getCurrentAnalysisId()));

  const dungRow = store.loadHistory().find(function (row) {
    return row.analysis_id === "id-a";
  });
  check("g205.old_row_immutable", dungRow && dungRow.data.useful_god.useful_display.indexOf("Thủy") !== -1, JSON.stringify(dungRow && dungRow.data && dungRow.data.useful_god));
  check("g205.created_at_is_analysis_time", dungRow && dungRow.created_at === "2026-08-21T01:00:00.000Z", dungRow && dungRow.created_at);
  check("g205.saved_at_not_view_time", dungRow && dungRow.saved_at === dungRow.created_at, dungRow && dungRow.saved_at);
  check("g205.version_metadata", dungRow && dungRow.customer_contract === "analysis_result.UsefulGodView@1.5", dungRow && dungRow.customer_contract);

  const fromList = store.resolveForDisplay(true, "id-a");
  check("g205.history_from_list_without_view", fromList && fromList.source === "history" && fromList.data.calendar.lunar_date === "DUNG", JSON.stringify(fromList));
  check("g205.current_survives_history_view", store.getCurrentAnalysisId() === "id-b", String(store.getCurrentAnalysisId()));
  check(
    "g205.missing_id_not_current",
    store.resolveForDisplay(true, "missing-id") == null,
    JSON.stringify(store.resolveForDisplay(true, "missing-id"))
  );
  check(
    "g205.normal_display_is_current",
    store.resolveForDisplay(false).analysis_id === "id-b",
    JSON.stringify(store.resolveForDisplay(false))
  );

  store.selectForView(dungRow);
  check("g205.explicit_history_selected", store.resolveForDisplay(true, "id-a").data.calendar.lunar_date === "DUNG", "");
  ctx.session.removeItem("bte_view_result");
  ctx.session.removeItem("bte_view_analysis_id");
  check(
    "g205.refresh_history_uses_snapshot",
    store.resolveForDisplay(true, "id-a").data.useful_god.useful_display.indexOf("Thủy") !== -1,
    JSON.stringify(store.resolveForDisplay(true, "id-a"))
  );

  const third = {
    analysis_id: "id-a-re",
    input: first.input,
    data: Object.assign({}, first.data, {
      analysis_id: "id-a-re",
      request_id: "id-a-re",
      calendar: { lunar_date: "REANALYZE", calendar_rule_version: "G1-10C" },
    }),
  };
  store.save(third);
  check("g205.reanalyze_creates_new_row", store.loadHistory().length === 3, String(store.loadHistory().length));
  const stillOld = store.loadHistory().find(function (row) {
    return row.analysis_id === "id-a";
  });
  check("g205.old_not_overwritten", stillOld && stillOld.data.calendar.lunar_date === "DUNG", JSON.stringify(stillOld));

  const withCorrupt = store.loadHistory().concat([
    { id: "bad", analysis_id: "bad", input: { year: 1990, month: 1, day: 1 }, data: null },
  ]);
  ctx.session.setItem("bte_history", JSON.stringify(withCorrupt));
  ctx.local.setItem("bte_history", JSON.stringify(withCorrupt));
  const corrupt = store.resolveForDisplay(true, "bad");
  check("g205.corrupt_not_current", corrupt && corrupt.corrupt === true && !corrupt.data, JSON.stringify(corrupt));
  check("g205.corrupt_does_not_replace_current", store.getCurrentAnalysisId() === "id-a-re", String(store.getCurrentAnalysisId()));

  const unversioned = {
    analysis_id: "legacy-1",
    input: { year: 1990, month: 1, day: 1 },
    data: { calendar: { lunar_date: "OLD" }, pattern: { dung_than: "Thủy" } },
  };
  store.saveHistory(unversioned);
  const legacy = store.loadHistory().find(function (row) {
    return row.analysis_id === "legacy-1";
  });
  check("g205.legacy_not_backfilled", legacy && legacy.customer_contract == null, JSON.stringify(legacy));
}

function testNarrativeV2ShadowIndependent() {
  const ctx = newStore();
  const payload = {
    input: { year: 1987, month: 1, day: 21 },
    data: {
      calendar: { lunar_date: "SHADOW", calendar_rule_version: "G1-10C" },
      narrative_result: { contract: "pack05_narrative_result_v1", status: "ok" },
      narrative_v2_shadow: { status: "ok", presentation: { status: "partial" }, replaces_pack05: false },
    },
  };
  ctx.store.save(payload);
  const loaded = ctx.store.load();
  check(
    "nimp10.pack05_preserved",
    loaded.data.narrative_result.contract === "pack05_narrative_result_v1",
    JSON.stringify(loaded.data.narrative_result)
  );
  check(
    "nimp10.shadow_preserved",
    loaded.data.narrative_v2_shadow.status === "ok",
    JSON.stringify(loaded.data.narrative_v2_shadow)
  );
  check(
    "nimp10.layers_distinct",
    loaded.data.narrative_result !== loaded.data.narrative_v2_shadow,
    ""
  );
  check(
    "nimp10.shadow_loader",
    ctx.store.loadNarrativeV2Shadow() && ctx.store.loadNarrativeV2Shadow().status === "ok",
    JSON.stringify(ctx.store.loadNarrativeV2Shadow())
  );
}

function testNarrativeProviderLayersStayIndependent() {
  const ctx = newStore();
  const payload = {
    input: { year: 1987, month: 1, day: 21 },
    data: {
      calendar: { lunar_date: "SWITCH", calendar_rule_version: "G1-10C" },
      narrative_result: { contract: "pack05_narrative_result_v1", status: "ok", summary: { identity: "pack05" } },
      narrative_v2_shadow: {
        status: "ok",
        presentation: { metadata: { version: "bte.presentation.v2.1" } },
        replaces_pack05: false,
      },
    },
  };
  ctx.store.save(payload);
  const before = ctx.store.selectNarrativeLayers();
  check("nrel01.layers_pack05", before.pack05 && before.pack05.contract === "pack05_narrative_result_v1", JSON.stringify(before.pack05));
  check("nrel01.layers_v2", before.narrative_v2 && before.narrative_v2.status === "ok", JSON.stringify(before.narrative_v2));
  const afterSwitch = ctx.store.selectNarrativeLayers();
  check(
    "nrel01.switch_does_not_mutate_pack05",
    JSON.stringify(afterSwitch.pack05) === JSON.stringify(before.pack05),
    JSON.stringify(afterSwitch.pack05)
  );
  check(
    "nrel01.switch_does_not_mutate_v2",
    JSON.stringify(afterSwitch.narrative_v2) === JSON.stringify(before.narrative_v2),
    JSON.stringify(afterSwitch.narrative_v2)
  );
  const reloaded = ctx.store.load();
  check(
    "nrel01.reload_preserves_both",
    reloaded.data.narrative_result.contract === "pack05_narrative_result_v1" &&
      reloaded.data.narrative_v2_shadow.status === "ok",
    JSON.stringify(reloaded.data)
  );
}

testKeysAreSeparate();
testFullFlowKeepsLastResult();
testSelectForViewNeverWritesLastKey();
testClearAndHistoryIsolation();
testLegacyKeysStillReadable();
testRejectsInvalidPayload();
testCurrentResultPrecedence();
testG205HistorySnapshotPolicy();
testNarrativeV2ShadowIndependent();
testNarrativeProviderLayersStayIndependent();

let failed = 0;
results.forEach(function (row) {
  if (row.ok) {
    process.stdout.write("PASS " + row.name + "\n");
  } else {
    failed += 1;
    process.stdout.write("FAIL " + row.name + ": " + row.detail + "\n");
  }
});
process.stdout.write("TOTAL " + results.length + " FAILED " + failed + "\n");
process.exit(failed ? 1 : 0);

