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
