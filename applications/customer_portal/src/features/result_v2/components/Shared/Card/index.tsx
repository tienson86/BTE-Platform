import type { ReactNode } from "react";
import type { DomainKey } from "../../../adapter/PortalResultModel";

export type ResultV2CardProps = {
  title?: ReactNode;
  footer?: ReactNode;
  children?: ReactNode;
  tone?: "default" | "warning" | "danger";
  className?: string;
  domain?: DomainKey;
  priority?: number | null;
  disabled?: boolean;
};

export function Card({
  title,
  footer,
  children,
  tone = "default",
  className,
  domain,
  priority,
  disabled = false,
}: ResultV2CardProps) {
  const classes = ["rv2-card", className].filter(Boolean).join(" ");
  return (
    <article
      className={classes}
      data-tone={tone}
      data-domain={domain}
      data-priority={priority ?? undefined}
      data-disabled={disabled ? "true" : undefined}
    >
      {title ? (
        <div className="rv2-card__header">
          {typeof title === "string" ? <h3 className="rv2-card__title">{title}</h3> : title}
        </div>
      ) : null}
      <div className="rv2-card__body">{children}</div>
      {footer ? <div className="rv2-card__footer">{footer}</div> : null}
    </article>
  );
}
