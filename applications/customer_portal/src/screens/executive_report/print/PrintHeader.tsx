/**
 * Running print header. Published title, customer, optional version only.
 */

import type { ReactNode } from "react";

type PrintHeaderProps = {
  readonly title: string;
  readonly customer: string;
  readonly version: string;
};

/**
 * Repeating header for print pages. Hidden on screen. No technical ids.
 */
export function PrintHeader({ title, customer, version }: PrintHeaderProps): ReactNode {
  return (
    <header className="bte-print__header" data-print="header">
      <span className="bte-print__header-title">{title}</span>
      {customer ? <span className="bte-print__header-customer">{customer}</span> : null}
      {version ? <span className="bte-print__header-version">{version}</span> : null}
    </header>
  );
}
