import type { ReactNode } from "react";
import { Container } from "../components/layout/Container";
import { cx } from "../utils";

export type AuthLayoutProps = {
  children?: ReactNode;
  title?: ReactNode;
  className?: string;
};

/** Minimal auth shell — no sidebar (WP03 / ADR-004). */
export function AuthLayout({ children, title, className }: AuthLayoutProps): ReactNode {
  return (
    <div className={cx("cui-auth-layout", className)}>
      <Container className="cui-auth-layout__panel" width="reading">
        {title ? <h1 className="cui-auth-layout__title">{title}</h1> : null}
        {children}
      </Container>
    </div>
  );
}
