import type { HTMLAttributes, ReactNode } from "react";
import { BaseText } from "../base";
import { cx } from "../../utils";

export type ReadingRailItem = {
  id: string;
  label: ReactNode;
  href: string;
  active?: boolean;
};

export type StickyReadingRailProps = Omit<HTMLAttributes<HTMLElement>, "title"> & {
  items: ReadingRailItem[];
  title?: ReactNode;
};

/** Shared sticky reading outline rail. */
export function StickyReadingRail({
  items,
  title = "Contents",
  className,
  ...rest
}: StickyReadingRailProps) {
  return (
    <nav
      className={cx("cui-shared-reading-rail", className)}
      aria-label={typeof title === "string" ? title : "Contents"}
      {...rest}
    >
      <BaseText variant="caption" tone="muted">
        {title}
      </BaseText>
      {items.map((item) => (
        <a
          key={item.id}
          href={item.href}
          className="cui-shared-reading-rail__link"
          data-active={item.active ? "true" : undefined}
          aria-current={item.active ? "location" : undefined}
        >
          {item.label}
        </a>
      ))}
    </nav>
  );
}
