import type { ReactNode } from "react";

type ShellSectionProps = {
  sectionId: string;
  testId: string;
  title: string;
  subtitle?: string;
};

export function ShellSection({
  sectionId,
  testId,
  title,
  subtitle,
}: ShellSectionProps): ReactNode {
  return (
    <section className="bte-card ne-shell-section" data-section={sectionId} data-testid={testId}>
      <h2>{title}</h2>
      {subtitle ? <p className="muted">{subtitle}</p> : null}
      <p className="muted ne-shell-placeholder">Phần này sẽ được dựng ở bước presentation tiếp theo.</p>
    </section>
  );
}
