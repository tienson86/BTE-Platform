import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

export function CreateDatasetPage() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [module, setModule] = useState("general");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const ds = await api.createDataset({ name, description, module });
      navigate(`/datasets/${ds.dataset_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Create failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-xl space-y-6">
      <div>
        <h2 className="font-display text-2xl">Create dataset</h2>
        <p className="text-sm text-[var(--muted)]">
          Start an empty draft golden dataset
        </p>
      </div>
      <form onSubmit={onSubmit} className="surface space-y-4 rounded-xl p-6">
        <label className="block space-y-1 text-sm">
          <span className="text-xs uppercase text-[var(--muted)]">Name</span>
          <input
            required
            className="w-full rounded-md border border-[var(--line)] bg-transparent px-3 py-2"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>
        <label className="block space-y-1 text-sm">
          <span className="text-xs uppercase text-[var(--muted)]">Module</span>
          <input
            className="w-full rounded-md border border-[var(--line)] bg-transparent px-3 py-2"
            value={module}
            onChange={(e) => setModule(e.target.value)}
          />
        </label>
        <label className="block space-y-1 text-sm">
          <span className="text-xs uppercase text-[var(--muted)]">
            Description
          </span>
          <textarea
            className="min-h-24 w-full rounded-md border border-[var(--line)] bg-transparent px-3 py-2"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </label>
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
          {busy ? "Creating…" : "Create draft"}
        </button>
      </form>
    </div>
  );
}
