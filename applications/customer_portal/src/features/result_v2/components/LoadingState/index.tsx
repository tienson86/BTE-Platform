import { memo } from "react";

export const LoadingState = memo(function LoadingState({ label }: { label: string }) {
  return (
    <div className="rv2-status-page rv2-loading" data-state="loading" role="status" aria-live="polite">
      <span className="rv2-loading__pulse" aria-hidden="true" />
      <p>{label}</p>
    </div>
  );
});
