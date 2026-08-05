from pathlib import Path

ROOT = Path("applications/customer_portal/src/components")
STYLES = Path("applications/customer_portal/src/styles/components/library")

def w(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(path)

# ---- DISPLAY ----
w(ROOT / "display/StatCard.tsx", '''
import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import { Card } from "../base/Card";
import { BaseText } from "../base/BaseText";

export type StatCardProps = HTMLAttributes<HTMLElement> & {
  label: ReactNode;
  value: ReactNode;
  hint?: ReactNode;
};

/** WP02 StatCard — compact statistic surface. */
export function StatCard({ label, value, hint, className, ...rest }: StatCardProps) {
  return (
    <Card className={cx("cui-stat-card", className)} {...rest}>
      <BaseText variant="caption" tone="secondary">
        {label}
      </BaseText>
      <BaseText variant="section">{value}</BaseText>
      {hint ? (
        <BaseText variant="metadata" tone="muted">
          {hint}
        </BaseText>
      ) : null}
    </Card>
  );
}
''')

w(ROOT / "display/InfoCard.tsx", '''
import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import { Card } from "../base/Card";
import { BaseText } from "../base/BaseText";

export type InfoCardProps = HTMLAttributes<HTMLElement> & {
  title: ReactNode;
  children?: ReactNode;
};

/** WP02 InfoCard — titled informational card. */
export function InfoCard({ title, children, className, ...rest }: InfoCardProps) {
  return (
    <Card title={title} className={cx("cui-info-card", className)} {...rest}>
      {typeof children === "string" ? (
        <BaseText variant="body">{children}</BaseText>
      ) : (
        children
      )}
    </Card>
  );
}
''')

w(ROOT / "display/MetricCard.tsx", '''
export { MetricCard } from "../shared/MetricCard";
export type { MetricCardProps } from "../shared/MetricCard";
''')

w(ROOT / "display/Timeline.tsx", '''
export { Timeline } from "../shared/Timeline";
export type { TimelineProps } from "../shared/Timeline";
''')

w(ROOT / "display/ScoreBar.tsx", '''
import type { HTMLAttributes } from "react";
import { cx } from "../../utils";
import { BaseProgress } from "../base/BaseProgress";
import { BaseText } from "../base/BaseText";

export type ScoreBarProps = HTMLAttributes<HTMLDivElement> & {
  label?: string;
  value: number;
  max?: number;
};

/** WP02 ScoreBar — labeled progress/score meter. */
export function ScoreBar({
  label,
  value,
  max = 100,
  className,
  ...rest
}: ScoreBarProps) {
  const clamped = Math.max(0, Math.min(value, max));
  return (
    <div className={cx("cui-score-bar", className)} {...rest}>
      {label ? (
        <div className="cui-score-bar__header">
          <BaseText variant="caption">{label}</BaseText>
          <BaseText variant="metadata" tone="muted">
            {clamped}/{max}
          </BaseText>
        </div>
      ) : null}
      <BaseProgress value={clamped} max={max} />
    </div>
  );
}
''')

w(ROOT / "display/ProgressBar.tsx", '''
export { BaseProgress as ProgressBar } from "../base/BaseProgress";
export type { BaseProgressProps as ProgressBarProps } from "../base/BaseProgress";
''')

w(ROOT / "display/SectionTitle.tsx", '''
export { SectionHeader as SectionTitle } from "../shared/SectionHeader";
export type { SectionHeaderProps as SectionTitleProps } from "../shared/SectionHeader";
''')

w(ROOT / "display/index.ts", '''
/**
 * WP02 Display Components.
 */

export { StatCard } from "./StatCard";
export type { StatCardProps } from "./StatCard";

export { InfoCard } from "./InfoCard";
export type { InfoCardProps } from "./InfoCard";

export { MetricCard } from "./MetricCard";
export type { MetricCardProps } from "./MetricCard";

export { Timeline } from "./Timeline";
export type { TimelineProps } from "./Timeline";

export { ScoreBar } from "./ScoreBar";
export type { ScoreBarProps } from "./ScoreBar";

export { ProgressBar } from "./ProgressBar";
export type { ProgressBarProps } from "./ProgressBar";

export { SectionTitle } from "./SectionTitle";
export type { SectionTitleProps } from "./SectionTitle";
''')

w(ROOT / "display/README.md", '''
# Display Components (WP02)

| Component | Props | Notes |
|-----------|-------|-------|
| StatCard | StatCardProps | |
| InfoCard | InfoCardProps | |
| MetricCard | MetricCardProps | Re-export shared |
| Timeline | TimelineProps | Re-export shared |
| ScoreBar | ScoreBarProps | |
| ProgressBar | BaseProgressProps | Alias |
| SectionTitle | SectionHeaderProps | Alias of SectionHeader |
''')

# ---- CHARTS ----
w(ROOT / "charts/ChartFrame.tsx", '''
import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import { Card } from "../base/Card";

export type ChartFrameProps = HTMLAttributes<HTMLElement> & {
  title?: ReactNode;
  children?: ReactNode;
};

/**
 * WP02 ChartFrame — layout shell for charts.
 * Does not render chart engines; host supplies visualization children.
 */
export function ChartFrame({ title, children, className, ...rest }: ChartFrameProps) {
  return (
    <Card title={title} className={cx("cui-chart-frame", className)} {...rest}>
      <div className="cui-chart-frame__canvas">{children}</div>
    </Card>
  );
}
''')

w(ROOT / "charts/index.ts", '''
/**
 * WP02 Charts — structural shells only (no chart library dependency).
 */

export { ChartFrame } from "./ChartFrame";
export type { ChartFrameProps } from "./ChartFrame";
''')

w(ROOT / "charts/README.md", '''
# Charts (WP02)

| Component | Props | Notes |
|-----------|-------|-------|
| ChartFrame | ChartFrameProps | Container only; no chart engine |

No external chart package added (ADR / Sprint rules).
''')

# ---- CSS ----
w(STYLES / "wp02.css", '''
/**
 * WP02 Component Library styles — token-driven only.
 */

.cui-card {
  border: var(--border-width) solid var(--border-divider);
  border-radius: var(--bte-radius-md, var(--radius-surface));
  box-shadow: var(--bte-shadow-sm, var(--elevation-soft));
  background: var(--surface-report-paper);
  padding: calc(var(--space-paragraph) * var(--space-scale));
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-list) * var(--space-scale));
}

.cui-card__title {
  font-family: var(--font-family-body);
  font-size: var(--font-section);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.cui-card__body {
  min-width: 0;
}

.cui-card__footer {
  border-top: var(--border-width) solid var(--border-divider);
  padding-top: calc(var(--space-list) * var(--space-scale));
}

.cui-icon-button {
  padding-inline: calc(var(--space-inline) * var(--space-scale));
  min-width: var(--touch-target-min);
}

.cui-toast {
  position: relative;
  z-index: var(--bte-z-toast, var(--z-toast));
  min-width: 240px;
  max-width: 420px;
  padding: calc(var(--space-list) * var(--space-scale));
  border-radius: var(--bte-radius-md, var(--radius-overlay));
  box-shadow: var(--bte-shadow-md, var(--elevation-overlay));
  background: var(--surface-overlay);
  border: var(--border-width) solid var(--border-divider);
  color: var(--text-primary);
}

.cui-toast[data-tone="success"] {
  border-color: var(--feedback-success);
  background: var(--feedback-success-soft);
}

.cui-toast[data-tone="warning"] {
  border-color: var(--feedback-warning);
  background: var(--feedback-warning-soft);
}

.cui-toast[data-tone="danger"] {
  border-color: var(--feedback-danger);
  background: var(--feedback-danger-soft);
}

.cui-toast[data-tone="info"] {
  border-color: var(--feedback-info);
  background: var(--feedback-info-soft);
}

.cui-toast__title {
  margin: 0;
  font-weight: var(--font-weight-semibold);
}

.cui-dialog-root,
.cui-drawer-root {
  position: fixed;
  inset: 0;
  z-index: var(--bte-z-modal, var(--z-modal));
  display: grid;
  place-items: center;
}

.cui-dialog-backdrop,
.cui-drawer-backdrop {
  position: absolute;
  inset: 0;
  border: 0;
  padding: 0;
  margin: 0;
  background: rgba(15, 23, 42, var(--opacity-overlay-scrim));
  cursor: pointer;
}

.cui-dialog {
  position: relative;
  z-index: 1;
  width: min(480px, calc(100% - var(--bte-space-32)));
  background: var(--surface-overlay);
  border-radius: var(--bte-radius-md, var(--radius-overlay));
  box-shadow: var(--bte-shadow-lg, var(--elevation-modal));
  padding: calc(var(--space-paragraph) * var(--space-scale));
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-list) * var(--space-scale));
}

.cui-dialog__title,
.cui-drawer__title {
  font-size: var(--font-section);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.cui-drawer-root {
  place-items: stretch;
  justify-items: end;
}

.cui-drawer-root[data-side="start"] {
  justify-items: start;
}

.cui-drawer {
  position: relative;
  z-index: 1;
  width: min(var(--rail-drawer-width), 100%);
  height: 100%;
  background: var(--surface-overlay);
  box-shadow: var(--bte-shadow-lg, var(--elevation-modal));
  padding: calc(var(--space-paragraph) * var(--space-scale));
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-list) * var(--space-scale));
}

.cui-pagination {
  display: inline-flex;
  align-items: center;
  gap: calc(var(--space-list) * var(--space-scale));
}

.cui-pagination__status {
  font-size: var(--font-caption);
  color: var(--text-secondary);
}

.cui-sidebar-item {
  display: flex;
  align-items: center;
  gap: calc(var(--space-inline) * var(--space-scale));
  min-height: var(--touch-target-min);
  padding-inline: calc(var(--space-list) * var(--space-scale));
  border-radius: var(--radius-control);
  color: var(--text-primary);
  text-decoration: none;
  background: transparent;
  border: 0;
  cursor: pointer;
  font: inherit;
  width: 100%;
  text-align: start;
  transition: background-color var(--bte-motion-fast, var(--motion-fast))
    var(--bte-motion-easing, var(--motion-ease-out));
}

.cui-sidebar-item:hover {
  background: var(--interaction-hover);
}

.cui-sidebar-item[data-active="true"] {
  background: var(--interaction-selected);
  color: var(--accent-primary);
}

.cui-topbar {
  display: flex;
  align-items: center;
  gap: calc(var(--space-list) * var(--space-scale));
  min-height: calc(var(--touch-target-min) + var(--bte-space-8));
  padding-inline: calc(var(--space-paragraph) * var(--space-scale));
  background: var(--surface-report-paper);
  border-bottom: var(--border-width) solid var(--border-divider);
  z-index: var(--bte-z-header, var(--z-sticky));
}

.cui-topbar__brand {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.cui-topbar__main {
  flex: 1;
  min-width: 0;
}

.cui-menu {
  list-style: none;
  margin: 0;
  padding: calc(var(--space-inline) * var(--space-scale));
  background: var(--surface-overlay);
  border: var(--border-width) solid var(--border-divider);
  border-radius: var(--bte-radius-md, var(--radius-overlay));
  box-shadow: var(--bte-shadow-md, var(--elevation-overlay));
}

.cui-dropdown {
  position: relative;
  display: inline-block;
}

.cui-dropdown__panel {
  position: absolute;
  top: calc(100% + var(--bte-space-4));
  inset-inline-start: 0;
  z-index: var(--bte-z-dropdown, var(--z-overlay));
  min-width: 180px;
}

.cui-score-bar {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-inline) * var(--space-scale));
}

.cui-score-bar__header {
  display: flex;
  justify-content: space-between;
  gap: calc(var(--space-list) * var(--space-scale));
}

.cui-chart-frame__canvas {
  min-height: 160px;
}

.cui-multi-select {
  min-height: calc(var(--touch-target-min) * 2);
}
''')

w(STYLES / "index.css", '''
@import "./wp02.css";
''')

print("display+charts+css done")
