import type { ReactNode } from "react";
import { Container } from "../components/layout/Container";
import { Stack } from "../components/layout/Stack";
import { cx } from "../utils";
import { AppBreadcrumb, type AppBreadcrumbItem } from "./Breadcrumb";

export type PageWrapperProps = {
  title?: ReactNode;
  description?: ReactNode;
  breadcrumb?: readonly AppBreadcrumbItem[];
  actions?: ReactNode;
  children?: ReactNode;
  className?: string;
};

/** Page content wrapper inside AppLayout (WP03). */
export function PageWrapper({
  title,
  description,
  breadcrumb,
  actions,
  children,
  className,
}: PageWrapperProps): ReactNode {
  return (
    <Container className={cx("cui-page-wrapper", className)} width="wide">
      <Stack gap="section">
        {breadcrumb ? <AppBreadcrumb items={breadcrumb} /> : null}
        {title || description || actions ? (
          <header className="cui-page-wrapper__header">
            <div className="cui-page-wrapper__heading">
              {title ? <h1 className="cui-page-wrapper__title">{title}</h1> : null}
              {description ? (
                <p className="cui-page-wrapper__description">{description}</p>
              ) : null}
            </div>
            {actions ? <div className="cui-page-wrapper__actions">{actions}</div> : null}
          </header>
        ) : null}
        <div className="cui-page-wrapper__body">{children}</div>
      </Stack>
    </Container>
  );
}
