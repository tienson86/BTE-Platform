import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../utils/cx";
import type { StatusTone } from "../tokens";

type DivProps = HTMLAttributes<HTMLDivElement> & { children?: ReactNode };

export function Card({ className, children, ...rest }: DivProps) {
  return (
    <div className={cx("bte-card", "bte-fade-in", className)} {...rest}>
      {children}
    </div>
  );
}

export function Panel({ className, children, ...rest }: DivProps) {
  return (
    <section className={cx("bte-panel", className)} {...rest}>
      {children}
    </section>
  );
}

export function MetricCard({
  label,
  value,
  hint,
  className,
  ...rest
}: DivProps & { label: string; value: ReactNode; hint?: string }) {
  return (
    <article className={cx("bte-metric-card", className)} {...rest}>
      <div className="bte-label">{label}</div>
      <div className="bte-metric">{value}</div>
      {hint ? <p className="bte-caption">{hint}</p> : null}
    </article>
  );
}

export function InfoCard({
  title,
  children,
  className,
  ...rest
}: DivProps & { title: string }) {
  return (
    <article className={cx("bte-info-card", "bte-stack-3", className)} {...rest}>
      <h3 className="bte-h3">{title}</h3>
      <div className="bte-body">{children}</div>
    </article>
  );
}

export function AnalysisCard({
  title,
  description,
  children,
  className,
  ...rest
}: DivProps & { title: string; description?: string }) {
  return (
    <section className={cx("bte-analysis-card", className)} {...rest}>
      <header className="bte-analysis-card-head">
        <h3 className="bte-h3">{title}</h3>
        {description ? <p className="bte-caption">{description}</p> : null}
      </header>
      <div className="bte-analysis-card-body">{children}</div>
    </section>
  );
}

export function SectionHeader({
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
    <div className={cx("bte-section-header", className)}>
      <div className="bte-stack-2">
        <h2 className="bte-h2">{title}</h2>
        {subtitle ? <p className="bte-caption">{subtitle}</p> : null}
      </div>
      {actions}
    </div>
  );
}

export function Divider({ className }: { className?: string }) {
  return <hr className={cx("bte-divider", className)} />;
}

export function StatusBadge({
  children,
  tone = "neutral",
  className,
}: {
  children: ReactNode;
  tone?: StatusTone;
  className?: string;
}) {
  return (
    <span className={cx("bte-badge", `bte-badge-${tone}`, className)}>
      {children}
    </span>
  );
}

export function ProgressBar({
  value,
  max = 100,
  className,
  label,
}: {
  value: number;
  max?: number;
  className?: string;
  label?: string;
}) {
  const pct = Math.max(0, Math.min(100, (value / (max || 100)) * 100));
  return (
    <div className={cx("bte-stack-2", className)} aria-label={label}>
      {label ? <div className="bte-caption">{label}</div> : null}
      <div className="bte-progress" role="progressbar" aria-valuenow={value} aria-valuemin={0} aria-valuemax={max}>
        <span style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

export function Gauge({
  value,
  label,
  className,
}: {
  value: number;
  label?: string;
  className?: string;
}) {
  const n = Math.max(0, Math.min(100, value));
  const r = 54;
  const cx0 = 70;
  const cy = 68;
  const start = Math.PI;
  const end = start + (0 - Math.PI) * (n / 100);
  const polar = (a: number) => ({ x: cx0 + Math.cos(a) * r, y: cy + Math.sin(a) * r });
  const p0 = polar(start);
  const p1 = polar(end);
  const large = n > 50 ? 1 : 0;
  const track = `M ${polar(Math.PI).x} ${polar(Math.PI).y} A ${r} ${r} 0 1 1 ${polar(0).x} ${polar(0).y}`;
  const arc = `M ${p0.x} ${p0.y} A ${r} ${r} 0 ${large} 1 ${p1.x} ${p1.y}`;
  return (
    <div className={cx("bte-gauge", className)}>
      <svg viewBox="0 0 140 90" role="img" aria-label={label || "gauge"}>
        <path className="bte-gauge-track" d={track} />
        <path className="bte-gauge-value" d={arc} />
        <text className="bte-gauge-num" x="70" y="62" textAnchor="middle">
          {Math.round(n)}
        </text>
        {label ? (
          <text className="bte-gauge-label" x="70" y="78" textAnchor="middle">
            {label}
          </text>
        ) : null}
      </svg>
    </div>
  );
}
