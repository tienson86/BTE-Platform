/**
 * Local expand/collapse state keyed by id. Does not mutate report.*.
 */

import { useCallback, useRef, useState } from "react";

export function useExpand(initial: Record<string, boolean> = {}) {
  const initialRef = useRef(initial);
  const [expanded, setExpanded] = useState<Record<string, boolean>>(() => ({
    ...initial,
  }));

  const isExpanded = useCallback((id: string, fallback = false): boolean => {
    if (id in expanded) return expanded[id];
    if (id in initialRef.current) return Boolean(initialRef.current[id]);
    return fallback;
  }, [expanded]);

  const toggle = useCallback((id: string, next?: boolean) => {
    setExpanded((current) => {
      const previous =
        id in current
          ? current[id]
          : Boolean(initialRef.current[id]);
      const value = next === undefined ? !previous : next;
      return { ...current, [id]: value };
    });
  }, []);

  const reset = useCallback(() => {
    setExpanded({ ...initialRef.current });
  }, []);

  return { expanded, isExpanded, toggle, reset };
}
