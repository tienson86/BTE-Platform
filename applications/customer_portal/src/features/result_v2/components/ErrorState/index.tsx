import { memo } from "react";
import { Button } from "../Shared/Button";
import { ResultIcon } from "../Shared/Icon";

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
    <div className="rv2-card rv2-status-page rv2-error-card" data-state="error" role="alert">
      <div className="rv2-error-card__mark" aria-hidden="true">
        <ResultIcon name="error" />
      </div>
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
