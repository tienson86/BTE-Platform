import { memo } from "react";
import { Button } from "../Shared/Button";

export type ErrorStateProps = {
  title: string;
  body: string;
  retryLabel?: string | null;
  onRetry?: () => void;
};

export const ErrorState = memo(function ErrorState({
  title,
  body,
  retryLabel,
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="rv2-card rv2-status-page" data-state="error" role="alert">
      <h2 className="rv2-section-header">{title}</h2>
      <p className="rv2-prose">{body}</p>
      {retryLabel && onRetry ? (
        <Button variant="secondary" onClick={onRetry}>
          {retryLabel}
        </Button>
      ) : null}
    </div>
  );
});
