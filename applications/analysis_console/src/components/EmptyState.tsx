import type { ReactNode } from "react";

type EmptyStateProps = {
  title: string;
  body: string;
  action?: ReactNode;
};

export function EmptyState({ title, body, action }: EmptyStateProps) {
  return (
    <div
      className="surface rounded-2xl px-6 py-10 text-center"
      role="status"
      aria-live="polite"
    >
      <h2 className="font-display text-2xl font-semibold">{title}</h2>
      <p className="mx-auto mt-2 max-w-md text-sm text-[var(--muted)]">{body}</p>
      {action ? <div className="mt-6 flex justify-center">{action}</div> : null}
    </div>
  );
}
