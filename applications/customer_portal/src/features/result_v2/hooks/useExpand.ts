/**
 * Local expand/collapse state keyed by id. Does not mutate report.*.
 */

import { useCallback, useState } from "react";

export function useExpand(initial: Record<string, boolean> = {}) {
  const [expanded, setExpanded] = useState<Record<string, boolean>>(initial);

  const isExpanded = useCallback(
    (id: string, fallback = false): boolean => {
      if (id in expanded) return expanded[id];
      return fallback;
    },
    [expanded],
  );

  const toggle = useCallback((id: string, next?: boolean) => {
    setExpanded((current) => {
      const previous = id in current ? current[id] : false;
      const value = next === undefined ? !previous : next;
      return { ...current, [id]: value };
    });
  }, []);

  const reset = useCallback(() => {
    setExpanded({});
  }, []);

  return { expanded, isExpanded, toggle, reset };
}
