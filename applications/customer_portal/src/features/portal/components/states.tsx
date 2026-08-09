import { PortalIcon } from "./Icon";
import { PvButton } from "./primitives";

export function PvEmpty({
  title,
  body,
  actionLabel,
  onAction,
}: {
  title: string;
  body: string;
  actionLabel?: string;
  onAction?: () => void;
}) {
  return (
    <div className="pv-card pv-state" data-state="empty">
      <PortalIcon name="empty" />
      <h2 className="pv-card-title">{title}</h2>
      <p className="pv-prose">{body}</p>
      {actionLabel && onAction ? (
        <PvButton variant="text" onClick={onAction}>
          {actionLabel}
        </PvButton>
      ) : null}
    </div>
  );
}

export function PvError({
  title,
  body,
  actionLabel,
  onAction,
}: {
  title: string;
  body: string;
  actionLabel?: string;
  onAction?: () => void;
}) {
  return (
    <div className="pv-card pv-state" data-state="error" role="alert">
      <PortalIcon name="error" />
      <h2 className="pv-card-title">{title}</h2>
      <p className="pv-prose">{body}</p>
      {actionLabel && onAction ? <PvButton onClick={onAction}>{actionLabel}</PvButton> : null}
    </div>
  );
}

export function PvLoading({ label }: { label: string }) {
  return (
    <div className="pv-state" data-state="loading" role="status" aria-live="polite">
      <span className="pv-skeleton__bar" aria-hidden="true" />
      <p>{label}</p>
    </div>
  );
}
