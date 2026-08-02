import { useId, useState, type ReactNode } from "react";
import { BaseSurface } from "../base";
import { cx } from "../../utils";

export type CollapsePanelProps = {
  title: ReactNode;
  children?: ReactNode;
  defaultOpen?: boolean;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  className?: string;
};

/** Shared collapsible panel. Local UI state only. */
export function CollapsePanel({
  title,
  children,
  defaultOpen = false,
  open,
  onOpenChange,
  className,
}: CollapsePanelProps) {
  const reactId = useId();
  const panelId = `collapse-panel-${reactId}`;
  const [uncontrolled, setUncontrolled] = useState(defaultOpen);
  const isOpen = open ?? uncontrolled;

  const setOpen = (next: boolean) => {
    if (open === undefined) {
      setUncontrolled(next);
    }
    onOpenChange?.(next);
  };

  return (
    <BaseSurface variant="section" className={cx("cui-shared-collapse", className)}>
      <button
        type="button"
        className="cui-shared-collapse__trigger"
        aria-expanded={isOpen}
        aria-controls={panelId}
        onClick={() => setOpen(!isOpen)}
      >
        <span>{title}</span>
        <span aria-hidden="true">{isOpen ? "−" : "+"}</span>
      </button>
      {isOpen ? (
        <div id={panelId} className="cui-shared-collapse__panel" role="region">
          {children}
        </div>
      ) : null}
    </BaseSurface>
  );
}
