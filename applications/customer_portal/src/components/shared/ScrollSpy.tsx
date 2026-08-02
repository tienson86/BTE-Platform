import { useEffect, useState, type ReactNode } from "react";
import { StickyReadingRail, type ReadingRailItem } from "./StickyReadingRail";

export type ScrollSpyItem = {
  id: string;
  label: ReactNode;
  targetId: string;
};

export type ScrollSpyProps = {
  items: ScrollSpyItem[];
  title?: ReactNode;
  rootMargin?: string;
  className?: string;
  onActiveChange?: (id: string | null) => void;
};

/** Shared scroll-spy outline. Observes section visibility only. */
export function ScrollSpy({
  items,
  title,
  rootMargin = "0px 0px -55% 0px",
  className,
  onActiveChange,
}: ScrollSpyProps) {
  const [activeId, setActiveId] = useState<string | null>(items[0]?.id ?? null);

  useEffect(() => {
    if (typeof IntersectionObserver === "undefined") {
      return;
    }
    const elements = items
      .map((item) => document.getElementById(item.targetId))
      .filter((el): el is HTMLElement => Boolean(el));
    if (!elements.length) {
      return;
    }
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (!visible?.target?.id) {
          return;
        }
        const match = items.find((item) => item.targetId === visible.target.id);
        if (!match) {
          return;
        }
        setActiveId(match.id);
        onActiveChange?.(match.id);
      },
      { rootMargin, threshold: [0.1, 0.25, 0.5] },
    );
    for (const el of elements) {
      observer.observe(el);
    }
    return () => observer.disconnect();
  }, [items, onActiveChange, rootMargin]);

  const railItems: ReadingRailItem[] = items.map((item) => ({
    id: item.id,
    label: item.label,
    href: `#${item.targetId}`,
    active: item.id === activeId,
  }));

  return <StickyReadingRail items={railItems} title={title} className={className} />;
}
