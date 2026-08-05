/**
 * Feedback layer — foundation boundaries + WP02 feedback components.
 */

export { ErrorBoundary } from "./ErrorBoundary";
export type { ErrorBoundaryProps } from "./ErrorBoundary";

export { LoadingBoundary } from "./LoadingBoundary";
export type { LoadingBoundaryProps } from "./LoadingBoundary";

export { logFoundationError } from "./logFoundationError";

export { Alert } from "./Alert";
export type { AlertProps } from "./Alert";

export { Toast } from "./Toast";
export type { ToastProps, ToastTone } from "./Toast";

export { Dialog } from "./Dialog";
export type { DialogProps } from "./Dialog";

export { Drawer } from "./Drawer";
export type { DrawerProps, DrawerSide } from "./Drawer";

export { Loading } from "./Loading";
export type { LoadingProps } from "./Loading";

export { Skeleton } from "./Skeleton";
export type { SkeletonProps } from "./Skeleton";

export { EmptyState } from "./EmptyState";
export type { EmptyStateProps } from "./EmptyState";

export { ErrorState } from "./ErrorState";
export type { ErrorStateProps } from "./ErrorState";
