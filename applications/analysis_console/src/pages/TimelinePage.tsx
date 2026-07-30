import { EmptyState } from "../components/EmptyState";
import { PageHeader } from "../components/PageHeader";
import { useLibrary } from "../state/library";

const TYPE_LABEL: Record<string, string> = {
  chart_created: "Chart",
  chart_opened: "Open",
  analysis_run: "Analysis",
  interpretation: "Interpretation",
  report: "Report",
  export: "Export",
  import: "Import",
  favorite: "Favorite",
  pin: "Pin",
};

export function TimelinePage() {
  const { timeline } = useLibrary();

  return (
    <div className="mx-auto max-w-3xl">
      <PageHeader
        eyebrow="Activity"
        title="Analysis Timeline"
        description="Chronological trail of chart, analysis, export, and library actions."
      />

      {timeline.length === 0 ? (
        <EmptyState
          title="Timeline is empty"
          body="Actions such as creating charts, favoriting, exporting, and importing appear here."
        />
      ) : (
        <ol className="relative space-y-4 border-l border-[var(--line)] pl-6">
          {timeline.map((event) => (
            <li key={event.id} className="relative">
              <span
                className="absolute -left-[1.55rem] top-1.5 h-3 w-3 rounded-full bg-[var(--accent)]"
                aria-hidden
              />
              <article className="surface rounded-2xl p-4">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded-full bg-[var(--accent-soft)] px-2.5 py-0.5 text-xs font-semibold text-[var(--accent)]">
                    {TYPE_LABEL[event.type] ?? event.type}
                  </span>
                  <time
                    className="text-xs text-[var(--muted)]"
                    dateTime={event.at}
                  >
                    {new Date(event.at).toLocaleString("vi-VN")}
                  </time>
                </div>
                <h2 className="mt-2 text-base font-semibold">{event.title}</h2>
                <p className="mt-1 text-sm text-[var(--muted)]">{event.detail}</p>
              </article>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
