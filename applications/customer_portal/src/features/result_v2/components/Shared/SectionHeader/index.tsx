import { ResultIcon, type ResultIconName } from "../Icon";

export function SectionHeader({
  id,
  children,
  icon,
}: {
  id?: string;
  children: string;
  icon?: ResultIconName;
}) {
  return (
    <h2 id={id} className="rv2-section-header">
      {icon ? <ResultIcon name={icon} /> : null}
      <span>{children}</span>
    </h2>
  );
}
