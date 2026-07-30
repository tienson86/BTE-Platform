import { Link } from "react-router-dom";
import { useSession } from "../state/session";

type LuckBlock = {
  current_age?: number;
  da_yun_sequence?: Array<{
    index?: number;
    stem?: string;
    branch?: string;
    start_age?: number;
    end_age?: number;
    label?: string;
  }>;
  liu_nian?: { stem?: string; branch?: string; year?: number; label?: string };
  liu_yue?: { stem?: string; branch?: string; month?: number; label?: string };
  liu_ri?: { stem?: string; branch?: string; day?: number; label?: string };
  liu_shi?: { stem?: string; branch?: string; hour?: number; label?: string };
};

export function LuckViewerPage() {
  const { chart, analysis } = useSession();

  if (!chart) {
    return (
      <div className="mx-auto max-w-lg surface rounded-2xl p-8 text-center">
        <h1 className="font-display text-3xl font-semibold">No luck data</h1>
        <p className="mt-3 text-sm text-[var(--muted)]">
          Create a chart to inspect Da Yun and Liu cycles.
        </p>
        <Link
          to="/chart/input"
          className="mt-6 inline-flex rounded-xl bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-white"
        >
          Chart Input
        </Link>
      </div>
    );
  }

  const luck = (chart.chart.luck ?? {}) as LuckBlock;
  const summary =
    analysis?.summary && typeof analysis.summary === "object"
      ? (analysis.summary as Record<string, unknown>)
      : null;

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <header className="fade-in">
        <h1 className="font-display text-3xl font-semibold md:text-4xl">
          Luck Viewer
        </h1>
        <p className="mt-2 text-sm text-[var(--muted)]">
          Timeline from chart.luck · Current age {luck.current_age ?? "—"}
        </p>
      </header>

      <section className="surface rounded-2xl p-5">
        <h2 className="font-display text-2xl font-semibold">Da Yun sequence</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          {(luck.da_yun_sequence ?? []).map((item, index) => (
            <div
              key={`${item.index ?? index}`}
              className="rounded-xl border border-[var(--line)] p-4"
            >
              <p className="text-xs uppercase text-[var(--muted)]">
                {item.label ?? `Da Yun ${item.index ?? index}`}
              </p>
              <p className="mt-2 text-lg font-medium">
                {item.stem} {item.branch}
              </p>
              <p className="mt-1 text-sm text-[var(--muted)]">
                Ages {item.start_age}–{item.end_age}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="surface grid gap-3 rounded-2xl p-5 sm:grid-cols-2">
        <Cycle
          title="Liu Nian"
          stem={luck.liu_nian?.stem}
          branch={luck.liu_nian?.branch}
          meta={luck.liu_nian?.year != null ? `Year ${luck.liu_nian.year}` : ""}
        />
        <Cycle
          title="Liu Yue"
          stem={luck.liu_yue?.stem}
          branch={luck.liu_yue?.branch}
          meta={
            luck.liu_yue?.month != null ? `Month ${luck.liu_yue.month}` : ""
          }
        />
        <Cycle
          title="Liu Ri"
          stem={luck.liu_ri?.stem}
          branch={luck.liu_ri?.branch}
          meta={luck.liu_ri?.day != null ? `Day ${luck.liu_ri.day}` : ""}
        />
        <Cycle
          title="Liu Shi"
          stem={luck.liu_shi?.stem}
          branch={luck.liu_shi?.branch}
          meta={luck.liu_shi?.hour != null ? `Hour ${luck.liu_shi.hour}` : ""}
        />
      </section>

      {summary ? (
        <section className="surface rounded-2xl p-5">
          <h2 className="font-display text-2xl font-semibold">
            Analysis summary snapshot
          </h2>
          <pre className="mt-4 overflow-x-auto rounded-xl border border-[var(--line)] p-4 text-xs">
            {JSON.stringify(summary, null, 2)}
          </pre>
        </section>
      ) : (
        <p className="text-sm text-[var(--muted)]">
          Run analysis to attach summary context alongside luck timeline.
        </p>
      )}
    </div>
  );
}

function Cycle({
  title,
  stem,
  branch,
  meta,
}: {
  title: string;
  stem?: string;
  branch?: string;
  meta: string;
}) {
  return (
    <div className="rounded-xl border border-[var(--line)] p-4">
      <p className="text-xs uppercase text-[var(--muted)]">{title}</p>
      <p className="mt-2 text-lg font-medium">
        {stem ?? "—"} {branch ?? ""}
      </p>
      {meta ? <p className="mt-1 text-sm text-[var(--muted)]">{meta}</p> : null}
    </div>
  );
}
