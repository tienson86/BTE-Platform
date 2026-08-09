import type { ReactNode } from "react";

export type ResultV2CardProps = {
  title?: ReactNode;
  footer?: ReactNode;
  children?: ReactNode;
  tone?: "default" | "warning" | "danger";
};

export function Card({ title, footer, children, tone = "default" }: ResultV2CardProps) {
  return (
    <article className="rv2-card" data-tone={tone}>
      {title ? <div className="rv2-card__title">{title}</div> : null}
      <div>{children}</div>
      {footer ? <div>{footer}</div> : null}
    </article>
  );
}
