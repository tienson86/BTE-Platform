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
"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

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
    data: { calendar: { solar_date: "21/01/1987", lunar_date: "22/12/" + tag } },
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

testKeysAreSeparate();
testFullFlowKeepsLastResult();
testSelectForViewNeverWritesLastKey();
testClearAndHistoryIsolation();
testLegacyKeysStillReadable();
testRejectsInvalidPayload();

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
