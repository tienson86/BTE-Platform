import type { ButtonHTMLAttributes, InputHTMLAttributes, ReactNode, SelectHTMLAttributes, TextareaHTMLAttributes } from "react";

export function PvButton({
  variant = "primary",
  children,
  type = "button",
  ...rest
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "text";
}) {
  return (
    <button type={type} className="pv-button" data-variant={variant} {...rest}>
      {children}
    </button>
  );
}

export function PvCard({
  title,
  footer,
  children,
  className,
}: {
  title?: ReactNode;
  footer?: ReactNode;
  children?: ReactNode;
  className?: string;
}) {
  return (
    <article className={["pv-card", className].filter(Boolean).join(" ")}>
      {title ? <div className="pv-card__header">{title}</div> : null}
      <div className="pv-card__body">{children}</div>
      {footer ? <div className="pv-card__footer">{footer}</div> : null}
    </article>
  );
}

export function PvInput({ label, hint, id, ...rest }: InputHTMLAttributes<HTMLInputElement> & { label: string; hint?: string }) {
  const inputId = id ?? label;
  return (
    <label className="pv-field" htmlFor={inputId}>
      <span className="pv-field__label">{label}</span>
      <input id={inputId} className="pv-input" {...rest} />
      {hint ? <span className="pv-field__hint">{hint}</span> : null}
    </label>
  );
}

export function PvSelect({
  label,
  id,
  children,
  ...rest
}: SelectHTMLAttributes<HTMLSelectElement> & { label: string; children: ReactNode }) {
  const inputId = id ?? label;
  return (
    <label className="pv-field" htmlFor={inputId}>
      <span className="pv-field__label">{label}</span>
      <select id={inputId} className="pv-input" {...rest}>
        {children}
      </select>
    </label>
  );
}

export function PvTextarea({
  label,
  id,
  ...rest
}: TextareaHTMLAttributes<HTMLTextAreaElement> & { label: string }) {
  const inputId = id ?? label;
  return (
    <label className="pv-field" htmlFor={inputId}>
      <span className="pv-field__label">{label}</span>
      <textarea id={inputId} className="pv-input pv-textarea" {...rest} />
    </label>
  );
}

export function PvCheckbox({ label, id, ...rest }: InputHTMLAttributes<HTMLInputElement> & { label: string }) {
  const inputId = id ?? label;
  return (
    <label className="pv-check" htmlFor={inputId}>
      <input id={inputId} type="checkbox" {...rest} />
      <span>{label}</span>
    </label>
  );
}

export function PvRadio({ label, id, ...rest }: InputHTMLAttributes<HTMLInputElement> & { label: string }) {
  const inputId = id ?? `${rest.name}-${rest.value}-${label}`;
  return (
    <label className="pv-check" htmlFor={inputId}>
      <input id={inputId} type="radio" {...rest} />
      <span>{label}</span>
    </label>
  );
}

export function PvSearch({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}) {
  return (
    <label className="pv-search">
      <span className="pv-sr-only">{label}</span>
      <input
        type="search"
        className="pv-input"
        value={value}
        placeholder={placeholder}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

export function PvBadge({ children, tone = "neutral" }: { children: ReactNode; tone?: "neutral" | "success" | "warning" }) {
  return (
    <span className="pv-badge" data-tone={tone}>
      {children}
    </span>
  );
}

export function PvTag({ children }: { children: ReactNode }) {
  return <span className="pv-tag">{children}</span>;
}

export function PvSkeleton({ label }: { label: string }) {
  return (
    <div className="pv-skeleton" role="status" aria-live="polite">
      <span className="pv-sr-only">{label}</span>
      <span className="pv-skeleton__bar" aria-hidden="true" />
      <span className="pv-skeleton__bar" aria-hidden="true" />
    </div>
  );
}

export function PvTabs({
  value,
  options,
  onChange,
}: {
  value: string;
  options: readonly { id: string; label: string }[];
  onChange: (id: string) => void;
}) {
  return (
    <div className="pv-tabs" role="tablist">
      {options.map((option) => (
        <button
          key={option.id}
          type="button"
          role="tab"
          className="pv-tabs__item"
          aria-selected={value === option.id}
          onClick={() => onChange(option.id)}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}

export function PvPagination({
  page,
  total,
  onPage,
}: {
  page: number;
  total: number;
  onPage: (page: number) => void;
}) {
  return (
    <div className="pv-pagination">
      <PvButton variant="secondary" disabled={page <= 1} onClick={() => onPage(page - 1)}>
        Trang trước
      </PvButton>
      <span className="pv-note">
        Trang {page} / {total}
      </span>
      <PvButton variant="secondary" disabled={page >= total} onClick={() => onPage(page + 1)}>
        Trang sau
      </PvButton>
    </div>
  );
}

export function PvDialog({
  open,
  title,
  children,
  onClose,
}: {
  open: boolean;
  title: string;
  children: ReactNode;
  onClose: () => void;
}) {
  if (!open) return null;
  return (
    <div className="pv-dialog-root" role="presentation">
      <button type="button" className="pv-dialog__backdrop" aria-label="Đóng hộp thoại" onClick={onClose} />
      <div className="pv-dialog" role="dialog" aria-modal="true" aria-labelledby="pv-dialog-title">
        <h2 id="pv-dialog-title" className="pv-section-title">
          {title}
        </h2>
        {children}
        <div className="pv-card__footer">
          <PvButton variant="secondary" onClick={onClose}>
            Đóng
          </PvButton>
        </div>
      </div>
    </div>
  );
}

export function PvDrawer({
  open,
  title,
  children,
  onClose,
}: {
  open: boolean;
  title: string;
  children: ReactNode;
  onClose: () => void;
}) {
  if (!open) return null;
  return (
    <div className="pv-drawer-root">
      <button type="button" className="pv-dialog__backdrop" aria-label="Đóng bảng bên" onClick={onClose} />
      <aside className="pv-drawer" aria-label={title}>
        <h2 className="pv-section-title">{title}</h2>
        {children}
      </aside>
    </div>
  );
}

export function PvTooltip({ label, children }: { label: string; children: ReactNode }) {
  return (
    <span className="pv-tooltip">
      {children}
      <span className="pv-tooltip__tip" role="tooltip">
        {label}
      </span>
    </span>
  );
}

export function PvToast({ message }: { message: string | null }) {
  if (!message) return null;
  return (
    <div className="pv-toast" role="status" aria-live="polite">
      {message}
    </div>
  );
}
