import { memo } from "react";
import { Button } from "../Shared/Button";
import { ResultIcon } from "../Shared/Icon";

export type EmptyStateProps = {
  title: string;
  body: string;
  nextLabel?: string | null;
  onNext?: () => void;
};

export const EmptyState = memo(function EmptyState({
  title,
  body,
  nextLabel,
  onNext,
}: EmptyStateProps) {
  return (
    <div className="rv2-card rv2-empty-card" data-state="empty">
      <div className="rv2-empty-card__mark" aria-hidden="true">
        <ResultIcon name="empty" />
      </div>
      <h3 className="rv2-card__title">{title}</h3>
      <p className="rv2-prose">{body}</p>
      {nextLabel && onNext ? (
        <Button variant="text" onClick={onNext}>
          {nextLabel}
        </Button>
      ) : null}
    </div>
  );
});
