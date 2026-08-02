import {
  useId,
  useState,
  type AnchorHTMLAttributes,
  type ButtonHTMLAttributes,
  type ReactNode,
} from "react";
import { cx } from "../utils/cx";
import type { StatusTone } from "../tokens";

export function Toolbar({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return <div className={cx("bte-toolbar", className)}>{children}</div>;
}

export function PageHeader({
  title,
  subtitle,
  actions,
  className,
}: {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  className?: string;
}) {
  return (
    <header className={cx("bte-page-header", "bte-fade-in", className)}>
      <div className="bte-stack-2">
        <h1 className="bte-h1">{title}</h1>
        {subtitle ? <p className="bte-subtitle">{subtitle}</p> : null}
      </div>
      {actions}
    </header>
  );
}

export type TabItem = { id: string; label: string };

export function Tabs({
  items,
  value,
  onChange,
  className,
}: {
  items: TabItem[];
  value: string;
  onChange: (id: string) => void;
  className?: string;
}) {
  return (
    <div className={cx("bte-tabs", className)} role="tablist">
      {items.map((item) => (
        <button
          key={item.id}
          type="button"
          role="tab"
          className="bte-tab"
          data-active={item.id === value}
          aria-selected={item.id === value}
          onClick={() => onChange(item.id)}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}

export function Accordion({
  title,
  children,
  defaultOpen = false,
  className,
}: {
  title: string;
  children: ReactNode;
  defaultOpen?: boolean;
  className?: string;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className={cx("bte-accordion", className)} data-open={open}>
      <button
        type="button"
        className="bte-accordion-head"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        <span>{title}</span>
        <span aria-hidden="true">{open ? "▾" : "▸"}</span>
      </button>
      <div className="bte-accordion-body bte-expand">{children}</div>
    </div>
  );
}

export function Collapse({
  title,
  children,
  open: controlledOpen,
  defaultOpen = true,
  onOpenChange,
  className,
}: {
  title: string;
  children: ReactNode;
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  className?: string;
}) {
  const [uncontrolled, setUncontrolled] = useState(defaultOpen);
  const open = controlledOpen ?? uncontrolled;
  const setOpen = (next: boolean) => {
    setUncontrolled(next);
    onOpenChange?.(next);
  };
  return (
    <div className={cx("bte-collapse", className)} data-open={open}>
      <button
        type="button"
        className="bte-collapse-head"
        aria-expanded={open}
        onClick={() => setOpen(!open)}
      >
        <span>{title}</span>
        <span aria-hidden="true">{open ? "▾" : "▸"}</span>
      </button>
      <div className="bte-collapse-body">{children}</div>
    </div>
  );
}

export function Alert({
  children,
  tone = "neutral",
  title,
  className,
}: {
  children: ReactNode;
  tone?: StatusTone;
  title?: string;
  className?: string;
}) {
  const toneClass =
    tone === "neutral" ? undefined : (`bte-alert-${tone}` as const);
  return (
    <div className={cx("bte-alert", toneClass, className)} role="status">
      {title ? <strong className="bte-subtitle">{title}</strong> : null}
      <div className="bte-body">{children}</div>
    </div>
  );
}

export function Tooltip({
  content,
  children,
  className,
}: {
  content: string;
  children: ReactNode;
  className?: string;
}) {
  const id = useId();
  return (
    <span className={cx("bte-tooltip", className)} aria-describedby={id}>
      {children}
      <span id={id} role="tooltip" className="bte-tooltip-bubble">
        {content}
      </span>
    </span>
  );
}

export function Skeleton({
  variant = "line",
  className,
}: {
  variant?: "line" | "card";
  className?: string;
}) {
  return (
    <div
      className={cx(
        "bte-skeleton",
        "bte-skeleton-pulse",
        variant === "card" ? "bte-skeleton-card" : "bte-skeleton-line",
        className,
      )}
      aria-hidden="true"
    />
  );
}

export function Loading({
  label = "Loading…",
  className,
}: {
  label?: string;
  className?: string;
}) {
  return (
    <div className={cx("bte-loading", "bte-stack-3", className)} role="status">
      <div className="bte-skeleton-pulse bte-skeleton-line" />
      <div className="bte-skeleton-pulse bte-skeleton-line" />
      <p className="bte-caption">{label}</p>
    </div>
  );
}

export function EmptyState({
  title,
  description,
  action,
  className,
}: {
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}) {
  return (
    <div className={cx("bte-empty", "bte-stack-3", className)}>
      <h3 className="bte-h3">{title}</h3>
      {description ? <p className="bte-caption">{description}</p> : null}
      {action}
    </div>
  );
}

export function ErrorState({
  title = "Something went wrong",
  description,
  action,
  className,
}: {
  title?: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}) {
  return (
    <div className={cx("bte-error", "bte-stack-3", className)} role="alert">
      <h3 className="bte-h3">{title}</h3>
      {description ? <p className="bte-body">{description}</p> : null}
      {action}
    </div>
  );
}

export function QuickAction({
  children,
  className,
  ...rest
}: AnchorHTMLAttributes<HTMLAnchorElement> & { href: string; children?: ReactNode }) {
  return (
    <a className={cx("bte-quick-action", className)} {...rest}>
      {children}
    </a>
  );
}

export function FloatingAction({
  label,
  className,
  ...rest
}: ButtonHTMLAttributes<HTMLButtonElement> & { label: string }) {
  return (
    <button
      type="button"
      className={cx("bte-fab", className)}
      aria-label={label}
      title={label}
      {...rest}
    >
      +
    </button>
  );
}
