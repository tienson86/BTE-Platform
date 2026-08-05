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
