import { Component, type ErrorInfo, type ReactNode } from "react";

import { logFoundationError } from "./logFoundationError";

export type ErrorBoundaryProps = {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
};

type ErrorBoundaryState = {
  hasError: boolean;
  error: Error | null;
};

/**
 * Presentation ErrorBoundary — catches render errors in the subtree.
 * No business recovery logic. Logging is a placeholder hook.
 */
export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  public state: ErrorBoundaryState = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    logFoundationError({
      error,
      componentStack: errorInfo.componentStack,
      boundary: "ErrorBoundary",
    });
    this.props.onError?.(error, errorInfo);
  }

  public render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback !== undefined) {
        return this.props.fallback;
      }
      return (
        <div
          className="cui-surface-callout cui-stack-paragraph"
          role="alert"
          aria-live="assertive"
        >
          <p className="cui-type-section">Something went wrong</p>
          <p className="cui-type-body cui-text-secondary">
            The presentation layer encountered an unexpected error. Please try again.
          </p>
        </div>
      );
    }
    return this.props.children;
  }
}
