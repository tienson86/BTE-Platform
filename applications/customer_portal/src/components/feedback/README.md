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
