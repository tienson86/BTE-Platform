import { memo } from "react";

export const LoadingState = memo(function LoadingState({ label }: { label: string }) {
  return (
    <div className="rv2-status-page" data-state="loading" role="status" aria-live="polite">
      <p>{label}</p>
    </div>
  );
});
