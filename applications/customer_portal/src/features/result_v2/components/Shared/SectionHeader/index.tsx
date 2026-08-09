export function SectionHeader({
  id,
  children,
}: {
  id?: string;
  children: string;
}) {
  return (
    <h2 id={id} className="rv2-section-header">
      {children}
    </h2>
  );
}
