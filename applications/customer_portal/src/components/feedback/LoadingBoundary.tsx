import type { ReactNode } from "react";

export type LoadingBoundaryProps = {
  children: ReactNode;
  loading?: boolean;
  fallback?: ReactNode;
  label?: string;
};

/**
 * Presentation LoadingBoundary — swaps children for a loading fallback.
 * No data fetching. No business logic.
 */
export function LoadingBoundary({
  children,
  loading = false,
  fallback,
  label = "Loading",
}: LoadingBoundaryProps): ReactNode {
  if (!loading) {
    return children;
  }

  if (fallback !== undefined) {
    return fallback;
  }

  return (
    <div
      className="cui-surface-section cui-inset-paragraph cui-stack-inline"
      role="status"
      aria-live="polite"
      aria-busy="true"
    >
      <p className="cui-type-body cui-text-secondary">{label}</p>
    </div>
  );
}
