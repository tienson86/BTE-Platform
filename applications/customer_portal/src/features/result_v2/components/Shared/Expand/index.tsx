import { ResultIcon } from "../Icon";

export type ExpandProps = {
  expanded: boolean;
  expandLabel: string;
  collapseLabel: string;
  controlsId: string;
  onToggle: () => void;
};

export function Expand({
  expanded,
  expandLabel,
  collapseLabel,
  controlsId,
  onToggle,
}: ExpandProps) {
  return (
    <button
      type="button"
      className="rv2-expand"
      aria-expanded={expanded}
      aria-controls={controlsId}
      onClick={onToggle}
    >
      <ResultIcon name="expand" />
      <span>{expanded ? collapseLabel : expandLabel}</span>
    </button>
  );
}
