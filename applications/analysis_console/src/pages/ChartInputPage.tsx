import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useSession } from "../state/session";

const DAY_MASTERS = [
  "Giáp",
  "Ất",
  "Bính",
  "Đinh",
  "Mậu",
  "Kỷ",
  "Canh",
  "Tân",
  "Nhâm",
  "Quý",
];

export function ChartInputPage() {
  const navigate = useNavigate();
  const { setChart, resetDownstreamFromChart } = useSession();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({
    full_name: "",
    day_master: "Giáp",
    year: 1990,
    month: 5,
    day: 15,
    hour: 10,
    minute: 0,
    gender: "male",
    timezone: "Asia/Ho_Chi_Minh",
  });

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const chart = await api.createChart({
        day_master: form.day_master,
        year: form.year,
        month: form.month,
        day: form.day,
        hour: form.hour,
        minute: form.minute,
        gender: form.gender,
        timezone: form.timezone,
        full_name: form.full_name || undefined,
      });
      setChart(chart);
      resetDownstreamFromChart();
      navigate("/chart");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create chart");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      <div className="fade-in surface rounded-[24px] p-6 md:p-8">
        <h1 className="font-display text-3xl font-semibold md:text-4xl">
          Chart Input
        </h1>
        <p className="mt-2 text-sm text-[var(--muted)]">
          Capture birth facts and Day Master. Luck timeline defaults are applied
          when omitted.
        </p>

        <form className="mt-8 space-y-5" onSubmit={onSubmit}>
          <label className="block space-y-2 text-sm">
            <span className="text-[var(--muted)]">Full name</span>
            <input
              className="w-full rounded-xl border border-[var(--line)] bg-transparent px-3 py-2.5 outline-none focus:border-[var(--accent)]"
              value={form.full_name}
              onChange={(e) => setForm({ ...form, full_name: e.target.value })}
              placeholder="Nguyễn Văn A"
            />
          </label>

          <label className="block space-y-2 text-sm">
            <span className="text-[var(--muted)]">Day Master</span>
            <select
              className="w-full rounded-xl border border-[var(--line)] bg-transparent px-3 py-2.5 outline-none focus:border-[var(--accent)]"
              value={form.day_master}
              onChange={(e) => setForm({ ...form, day_master: e.target.value })}
            >
              {DAY_MASTERS.map((dm) => (
                <option key={dm} value={dm}>
                  {dm}
                </option>
              ))}
            </select>
          </label>

          <div className="grid grid-cols-2 gap-3 md:grid-cols-3">
            {(
              [
                ["year", form.year],
                ["month", form.month],
                ["day", form.day],
                ["hour", form.hour],
                ["minute", form.minute],
              ] as const
            ).map(([key, value]) => (
              <label key={key} className="block space-y-2 text-sm">
                <span className="capitalize text-[var(--muted)]">{key}</span>
                <input
                  type="number"
                  className="w-full rounded-xl border border-[var(--line)] bg-transparent px-3 py-2.5 outline-none focus:border-[var(--accent)]"
                  value={value}
                  onChange={(e) =>
                    setForm({ ...form, [key]: Number(e.target.value) })
                  }
                />
              </label>
            ))}
            <label className="block space-y-2 text-sm">
              <span className="text-[var(--muted)]">Gender</span>
              <select
                className="w-full rounded-xl border border-[var(--line)] bg-transparent px-3 py-2.5 outline-none focus:border-[var(--accent)]"
                value={form.gender}
                onChange={(e) => setForm({ ...form, gender: e.target.value })}
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </label>
          </div>

          {error ? (
            <p className="text-sm text-[var(--danger)]">{error}</p>
          ) : null}

          <button
            type="submit"
            disabled={busy}
            className="w-full rounded-xl bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-white transition hover:opacity-90 disabled:opacity-60"
          >
            {busy ? "Creating…" : "Create Chart"}
          </button>
        </form>
      </div>
    </div>
  );
}
