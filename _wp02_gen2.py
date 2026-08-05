from pathlib import Path

ROOT = Path("applications/customer_portal/src/components")

def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(path)

# ---- LAYOUT ----
w("layout/Stack.tsx", '''
export { BaseStack as Stack } from "../base/BaseStack";
export type { BaseStackProps as StackProps } from "../base/BaseStack";
''')

w("layout/Container.tsx", '''
export { BaseContainer as Container } from "../base/BaseContainer";
export type { BaseContainerProps as ContainerProps, BaseContainerWidth as ContainerWidth } from "../base/BaseContainer";
''')

w("layout/Grid.tsx", '''
export { BaseGrid as Grid } from "../base/BaseGrid";
export type { BaseGridProps as GridProps, BaseGridColumns as GridColumns } from "../base/BaseGrid";
''')

w("layout/index.ts", '''
/**
 * WP02 Layout primitives.
 */

export { Stack } from "./Stack";
export type { StackProps } from "./Stack";

export { Container } from "./Container";
export type { ContainerProps, ContainerWidth } from "./Container";

export { Grid } from "./Grid";
export type { GridProps, GridColumns } from "./Grid";
''')

w("layout/README.md", '''
# Layout Components (WP02)

| Component | Props | Notes |
|-----------|-------|-------|
| Stack | BaseStackProps | Vertical/horizontal stack |
| Container | BaseContainerProps | Width-constrained wrapper |
| Grid | BaseGridProps | CSS grid helper |

```tsx
import { Stack, Container } from "@/components/layout";
<Container><Stack gap="section">...</Stack></Container>
```
''')

# ---- FEEDBACK additions ----
w("feedback/Alert.tsx", '''
export { BaseAlert as Alert } from "../base/BaseAlert";
export type { BaseAlertProps as AlertProps } from "../base/BaseAlert";
''')

w("feedback/Loading.tsx", '''
export { BaseLoadingState as Loading } from "../base/BaseLoadingState";
export type { BaseLoadingStateProps as LoadingProps } from "../base/BaseLoadingState";
''')

w("feedback/Skeleton.tsx", '''
export { BaseSkeleton as Skeleton } from "../base/BaseSkeleton";
export type { BaseSkeletonProps as SkeletonProps } from "../base/BaseSkeleton";
''')

w("feedback/EmptyState.tsx", '''
export { BaseEmptyState as EmptyState } from "../base/BaseEmptyState";
export type { BaseEmptyStateProps as EmptyStateProps } from "../base/BaseEmptyState";
''')

w("feedback/ErrorState.tsx", '''
export { BaseErrorState as ErrorState } from "../base/BaseErrorState";
export type { BaseErrorStateProps as ErrorStateProps } from "../base/BaseErrorState";
''')

w("feedback/Toast.tsx", '''
import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type ToastTone = "neutral" | "success" | "warning" | "danger" | "info";

export type ToastProps = HTMLAttributes<HTMLDivElement> & {
  tone?: ToastTone;
  title?: ReactNode;
  children?: ReactNode;
  open?: boolean;
};

/** WP02 Toast — presentational toast surface (host manages open state). */
export function Toast({
  tone = "info",
  title,
  children,
  open = true,
  className,
  role = "status",
  ...rest
}: ToastProps) {
  if (!open) {
    return null;
  }
  return (
    <div
      className={cx("cui-toast", className)}
      data-tone={tone}
      role={role}
      {...rest}
    >
      {title ? <p className="cui-toast__title">{title}</p> : null}
      {children ? <div className="cui-toast__body">{children}</div> : null}
    </div>
  );
}
''')

w("feedback/Dialog.tsx", '''
import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import { BaseButton } from "../base/BaseButton";

export type DialogProps = HTMLAttributes<HTMLDivElement> & {
  open: boolean;
  title?: ReactNode;
  children?: ReactNode;
  onClose?: () => void;
  closeLabel?: string;
};

/** WP02 Dialog — presentational modal dialog (caller controls open). */
export function Dialog({
  open,
  title,
  children,
  onClose,
  closeLabel = "Close",
  className,
  ...rest
}: DialogProps) {
  if (!open) {
    return null;
  }
  return (
    <div className="cui-dialog-root" role="presentation">
      <button
        type="button"
        className="cui-dialog-backdrop"
        aria-label={closeLabel}
        onClick={onClose}
      />
      <div
        className={cx("cui-dialog", className)}
        role="dialog"
        aria-modal="true"
        aria-label={typeof title === "string" ? title : undefined}
        {...rest}
      >
        {title ? <div className="cui-dialog__title">{title}</div> : null}
        <div className="cui-dialog__body">{children}</div>
        {onClose ? (
          <div className="cui-dialog__footer">
            <BaseButton variant="secondary" onClick={onClose}>
              {closeLabel}
            </BaseButton>
          </div>
        ) : null}
      </div>
    </div>
  );
}
''')

w("feedback/Drawer.tsx", '''
import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import { BaseButton } from "../base/BaseButton";

export type DrawerSide = "start" | "end";

export type DrawerProps = HTMLAttributes<HTMLDivElement> & {
  open: boolean;
  title?: ReactNode;
  children?: ReactNode;
  side?: DrawerSide;
  onClose?: () => void;
  closeLabel?: string;
};

/** WP02 Drawer — slide-over panel (caller controls open). */
export function Drawer({
  open,
  title,
  children,
  side = "end",
  onClose,
  closeLabel = "Close",
  className,
  ...rest
}: DrawerProps) {
  if (!open) {
    return null;
  }
  return (
    <div className="cui-drawer-root" data-side={side} role="presentation">
      <button
        type="button"
        className="cui-drawer-backdrop"
        aria-label={closeLabel}
        onClick={onClose}
      />
      <aside
        className={cx("cui-drawer", className)}
        role="dialog"
        aria-modal="true"
        {...rest}
      >
        {title ? <div className="cui-drawer__title">{title}</div> : null}
        <div className="cui-drawer__body">{children}</div>
        {onClose ? (
          <div className="cui-drawer__footer">
            <BaseButton variant="secondary" onClick={onClose}>
              {closeLabel}
            </BaseButton>
          </div>
        ) : null}
      </aside>
    </div>
  );
}
''')

# Update feedback/index.ts — read existing first via rewrite full file
w("feedback/index.ts", '''
/**
 * Feedback layer — foundation boundaries + WP02 feedback components.
 */

export { ErrorBoundary } from "./ErrorBoundary";
export type { ErrorBoundaryProps } from "./ErrorBoundary";

export { LoadingBoundary } from "./LoadingBoundary";
export type { LoadingBoundaryProps, LoadingBoundaryRenderState } from "./LoadingBoundary";

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
''')

w("feedback/README.md", '''
# Feedback Components (WP02)

| Component | Props | Notes |
|-----------|-------|-------|
| Alert | BaseAlertProps | Inline alert |
| Toast | ToastProps | Host manages `open` |
| Dialog | DialogProps | Modal; host manages `open` |
| Drawer | DrawerProps | Slide-over |
| Loading | BaseLoadingStateProps | |
| Skeleton | BaseSkeletonProps | |
| EmptyState | BaseEmptyStateProps | |
| ErrorState | BaseErrorStateProps | |

Also exports foundation: ErrorBoundary, LoadingBoundary.

```tsx
import { Dialog, Toast } from "@/components/feedback";
<Dialog open={open} title="Confirm" onClose={() => setOpen(false)}>...</Dialog>
```
''')

print("layout+feedback done")
