import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

const SAMPLE = `{
  "name": "Imported Strength Pack",
  "module": "strength",
  "description": "Imported via Validation Console",
  "cases": [
    {
      "case_id": "case_1001",
      "description": "Imported strong case",
      "input_fixture": { "note": "sample" },
      "expected_output": { "strength": "strong" },
      "actual_output": { "strength": "strong" },
      "tags": ["imported", "canonical"],
      "coverage_goal": "canonical"
    }
  ]
}`;

export function ImportDatasetPage() {
  const navigate = useNavigate();
  const [jsonText, setJsonText] = useState(SAMPLE);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const parsed = JSON.parse(jsonText) as {
        name?: string;
        module?: string;
        description?: string;
        cases?: unknown[];
      };
      if (!parsed.name || !Array.isArray(parsed.cases)) {
        throw new Error("JSON must include name and cases[]");
      }
      const ds = await api.importDataset({
        name: parsed.name,
        module: parsed.module,
        description: parsed.description,
        cases: parsed.cases as never[],
      });
      navigate(`/datasets/${ds.dataset_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Import failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h2 className="font-display text-2xl">Import dataset</h2>
        <p className="text-sm text-[var(--muted)]">
          Paste a JSON bundle with name and cases
        </p>
      </div>
      <form onSubmit={onSubmit} className="surface space-y-4 rounded-xl p-6">
        <textarea
          className="min-h-80 w-full rounded-md border border-[var(--line)] bg-transparent px-3 py-2 font-mono text-xs"
          value={jsonText}
          onChange={(e) => setJsonText(e.target.value)}
          spellCheck={false}
        />
        {error ? (
          <p className="text-sm text-[var(--danger)]" role="alert">
            {error}
          </p>
        ) : null}
        <button
          type="submit"
          disabled={busy}
          className="rounded-md bg-[var(--accent)] px-4 py-2 text-sm text-white disabled:opacity-60"
        >
          {busy ? "Importing…" : "Import"}
        </button>
      </form>
    </div>
  );
}
