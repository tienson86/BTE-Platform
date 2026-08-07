/**
 * PACK_04 — Shared fixed-height Presentation Card.
 * Height is locked by card type; dynamic content cannot expand the shell.
 */

import type { HTMLAttributes, ReactNode } from "react";
import {
  CARD_HEIGHT_PX,
  OVERFLOW_BY_CARD_TYPE,
  type PresentationCardType,
  type ResultSectionId,
  cardTypeForSection,
} from "../../presentation";
import { cx } from "../../utils";

export type PresentationCardProps = HTMLAttributes<HTMLElement> & {
  /** Fixed-height card category. */
  cardType?: PresentationCardType;
  /** Canonical Result section — resolves cardType when provided. */
  section?: ResultSectionId;
  /** Optional header slot (title). */
  header?: ReactNode;
  /** Optional footer slot (CTA / hasMore). */
  footer?: ReactNode;
  /** Show hasMore affordance styling on footer. */
  hasMore?: boolean;
  as?: "section" | "article" | "div";
  children?: ReactNode;
};

/**
 * Fixed-height card shell for Result presentation surfaces.
 */
export function PresentationCard({
  cardType,
  section,
  header,
  footer,
  hasMore = false,
  as = "section",
  className,
  children,
  style,
  ...rest
}: PresentationCardProps): ReactNode {
  const resolvedType: PresentationCardType =
    cardType ?? (section ? cardTypeForSection(section) : "preview");
  const height = CARD_HEIGHT_PX[resolvedType];
  const overflow = OVERFLOW_BY_CARD_TYPE[resolvedType];
  const Component = as;

  return (
    <Component
      className={cx("ui-presentation-card", className)}
      data-presentation="pack04"
      data-card-type={resolvedType}
      data-section={section}
      data-overflow-title={overflow.title}
      data-overflow-body={overflow.body}
      data-has-more={hasMore ? "true" : "false"}
      style={{
        ...style,
        ["--ui-card-height" as string]: `${height}px`,
      }}
      {...rest}
    >
      {header ? (
        <div className="ui-presentation-card__header" data-slot="header">
          {header}
        </div>
      ) : null}
      <div
        className="ui-presentation-card__body"
        data-slot="body"
        data-overflow={overflow.body}
      >
        {children}
      </div>
      {footer ? (
        <div className="ui-presentation-card__footer" data-slot="footer">
          {footer}
        </div>
      ) : null}
    </Component>
  );
}
