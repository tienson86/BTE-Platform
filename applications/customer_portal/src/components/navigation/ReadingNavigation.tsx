import type { ReactNode } from "react";
import { SectionContainer, SectionDivider } from "../shared";
import type { NavigationReadyViewModel } from "../../view_models/navigation";
import { cx } from "../../utils";
import { AnchorNavigation } from "./AnchorNavigation";
import { BackToTop } from "./BackToTop";
import { CurrentSection } from "./CurrentSection";
import { JumpNavigator } from "./JumpNavigator";
import { PrintNavigator } from "./PrintNavigator";
import { ReadingBreadcrumb } from "./ReadingBreadcrumb";
import { ReadingProgress } from "./ReadingProgress";
import { ReadingRail } from "./ReadingRail";
import { ScrollSpy } from "./ScrollSpy";
import { TableOfContents } from "./TableOfContents";

export type ReadingNavigationProps = {
  data: NavigationReadyViewModel;
  children?: ReactNode;
  className?: string;
};

/**
 * Reading Navigation shell — Pack 06 WP-0011.
 * Coordinates presentation flow; does not alter frozen screen content.
 */
export function ReadingNavigation({
  data,
  children,
  className,
}: ReadingNavigationProps) {
  const title = data.title ?? "Reading Navigation";

  return (
    <div className={cx("cui-nav-reading-navigation", className)} aria-label={title}>
      <a className="cui-nav-skip-link" href="#cui-nav-main-content">
        Skip to content
      </a>

      <aside className="cui-nav-reading-navigation__chrome" aria-label="Reading aids">
        <ReadingBreadcrumb items={data.breadcrumbs} />
        <CurrentSection data={data.currentSection} />
        <ReadingProgress value={data.progress} />
        <ReadingRail items={data.items} title={data.railTitle ?? "Reading Rail"} />
        <TableOfContents items={data.toc} title={data.tocTitle ?? "Table of Contents"} />
        <ScrollSpy items={data.items} title="Scroll Spy" />
        <JumpNavigator items={data.jumpTargets} />
        <AnchorNavigation items={data.anchors} />
      </aside>

      <SectionDivider className="cui-nav-reading-navigation__divider" />

      <SectionContainer
        id="cui-nav-main-content"
        width="reading"
        gap="section"
        className="cui-nav-reading-navigation__content"
        tabIndex={-1}
      >
        {children}
      </SectionContainer>

      <PrintNavigator data={data.print} />
      <BackToTop data={data.backToTop} />
    </div>
  );
}
