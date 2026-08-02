import { SectionHeader, StatusBadge, TagGroup } from "../shared";
import { cx } from "../../utils";

export type PillarHeaderProps = {
  title: string;
  isDayMaster?: boolean;
  tenGodLabels?: string[];
  className?: string;
};

/** Pillar column header with optional Day Master emphasis. */
export function PillarHeader({
  title,
  isDayMaster = false,
  tenGodLabels = [],
  className,
}: PillarHeaderProps) {
  return (
    <div className={cx("cui-biz-pillar-header", className)}>
      <SectionHeader
        title={title}
        level={3}
        actions={
          isDayMaster ? <StatusBadge status="accent">Day Master</StatusBadge> : undefined
        }
      />
      {tenGodLabels.length > 0 ? (
        <TagGroup label={`${title} ten gods`}>
          {tenGodLabels.map((label) => (
            <StatusBadge key={`${title}-${label}`} status="info">
              {label}
            </StatusBadge>
          ))}
        </TagGroup>
      ) : null}
    </div>
  );
}
