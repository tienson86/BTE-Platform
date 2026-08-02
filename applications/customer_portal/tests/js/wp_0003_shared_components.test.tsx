import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  Accordion,
  Callout,
  ChipGroup,
  CitationRow,
  CollapsePanel,
  ConfidenceBadge,
  EmptyState,
  ErrorState,
  EvidenceList,
  EvidenceRow,
  FilterBar,
  FooterNote,
  GlossaryEntry,
  HighlightBox,
  InformationBox,
  InsightBox,
  KeyValueGrid,
  KeyValueRow,
  LabelValueRow,
  LoadingState,
  MetricCard,
  MetricGroup,
  MetricRow,
  PropertyGrid,
  PropertyItem,
  ReadingProgress,
  ReferenceBlock,
  SearchBar,
  SectionContainer,
  SectionDivider,
  SectionHeader,
  SectionSurface,
  SkeletonMetric,
  SkeletonParagraph,
  SkeletonSection,
  StatusBadge,
  StickyReadingRail,
  SuccessBox,
  TabPanel,
  TagGroup,
  Timeline,
  TimelineItem,
  Toolbar,
  UnavailableState,
  WarningBox,
  sharedComponentsWorkPackageId,
  BaseTag,
  BaseChip,
  BaseButton,
} from "../../src";

afterEach(() => {
  cleanup();
});

describe("WP-0003 Shared Components", () => {
  it("exports WP-0003 identity", () => {
    expect(sharedComponentsWorkPackageId).toBe("WP-0003");
  });

  it("renders section primitives composed from base", () => {
    render(
      <SectionContainer>
        <SectionHeader title="Chapter" subtitle="Overview" actions={<BaseButton>Action</BaseButton>} />
        <SectionDivider />
        <SectionSurface>
          <LabelValueRow label="Field" value="Value" />
        </SectionSurface>
      </SectionContainer>,
    );
    expect(screen.getByRole("heading", { name: "Chapter" })).toBeTruthy();
    expect(screen.getByText("Overview")).toBeTruthy();
    expect(screen.getByRole("button", { name: "Action" })).toBeTruthy();
    expect(screen.getByText("Field")).toBeTruthy();
  });

  it("renders metric and property patterns", () => {
    render(
      <>
        <MetricGroup columns={2}>
          <MetricCard label="Score" value="82" hint="stable" />
          <MetricRow label="Strength" value="High" />
        </MetricGroup>
        <PropertyGrid columns={2}>
          <PropertyItem label="Stem" value="Jia" />
        </PropertyGrid>
        <KeyValueGrid>
          <KeyValueRow label="Key" value="Value" />
        </KeyValueGrid>
      </>,
    );
    expect(screen.getByText("Score")).toBeTruthy();
    expect(screen.getByText("82")).toBeTruthy();
    expect(screen.getByText("Strength")).toBeTruthy();
    expect(screen.getByText("Stem")).toBeTruthy();
    expect(screen.getByText("Key")).toBeTruthy();
  });

  it("renders badges, evidence, boxes, and callout", () => {
    render(
      <>
        <StatusBadge status="success">Ready</StatusBadge>
        <ConfidenceBadge level="high" />
        <EvidenceList>
          <EvidenceRow label="Rule A" detail="detail" meta="E1" />
        </EvidenceList>
        <HighlightBox title="Highlight">Body</HighlightBox>
        <InformationBox title="Info">Info body</InformationBox>
        <WarningBox title="Warn">Warn body</WarningBox>
        <SuccessBox title="Ok">Ok body</SuccessBox>
        <InsightBox title="Insight">Insight body</InsightBox>
        <Callout title="Note">Callout body</Callout>
      </>,
    );
    expect(screen.getByText("Ready")).toBeTruthy();
    expect(screen.getByText("high")).toBeTruthy();
    expect(screen.getByText("Rule A")).toBeTruthy();
    expect(screen.getByText("Highlight")).toBeTruthy();
    expect(screen.getByText("Info")).toBeTruthy();
    expect(screen.getByText("Warn")).toBeTruthy();
    expect(screen.getByText("Ok")).toBeTruthy();
    expect(screen.getByText("Insight")).toBeTruthy();
    expect(screen.getByText("Note")).toBeTruthy();
  });

  it("supports reading progress and sticky rail", () => {
    render(
      <>
        <ReadingProgress value={35} />
        <StickyReadingRail
          items={[
            { id: "a", label: "One", href: "#one", active: true },
            { id: "b", label: "Two", href: "#two" },
          ]}
        />
      </>,
    );
    expect(screen.getByRole("progressbar")).toBeTruthy();
    expect(screen.getByRole("navigation")).toBeTruthy();
    expect(screen.getByRole("link", { name: "One" }).getAttribute("aria-current")).toBe(
      "location",
    );
  });

  it("supports collapse, accordion, and tabs interactions", () => {
    render(
      <>
        <CollapsePanel title="More">Hidden details</CollapsePanel>
        <Accordion
          items={[
            { id: "1", title: "Item 1", content: "Content 1" },
            { id: "2", title: "Item 2", content: "Content 2" },
          ]}
        />
        <TabPanel
          items={[
            { id: "t1", label: "Tab A", content: "Panel A" },
            { id: "t2", label: "Tab B", content: "Panel B" },
          ]}
        />
      </>,
    );

    fireEvent.click(screen.getByRole("button", { name: /More/ }));
    expect(screen.getByText("Hidden details")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: /Item 1/ }));
    expect(screen.getByText("Content 1")).toBeTruthy();

    expect(screen.getByRole("tab", { name: "Tab A" }).getAttribute("aria-selected")).toBe("true");
    fireEvent.click(screen.getByRole("tab", { name: "Tab B" }));
    expect(screen.getByText("Panel B")).toBeTruthy();
  });

  it("renders timeline and semantic states", () => {
    render(
      <>
        <Timeline>
          <TimelineItem title="Event" description="Desc" meta="2020" />
        </Timeline>
        <EmptyState title="Empty" />
        <UnavailableState title="Unavailable" />
        <LoadingState title="Loading" />
        <ErrorState title="Error" />
      </>,
    );
    expect(screen.getByText("Event")).toBeTruthy();
    expect(screen.getByText("Empty")).toBeTruthy();
    expect(screen.getByText("Unavailable")).toBeTruthy();
    expect(screen.getByRole("status", { name: "Loading" })).toBeTruthy();
    expect(screen.getByText("Error")).toBeTruthy();
  });

  it("supports search, filter, toolbar callbacks", () => {
    const onSearch = vi.fn();
    render(
      <>
        <SearchBar onSearch={onSearch} defaultValue="bazi" />
        <FilterBar>
          <BaseButton>Filter</BaseButton>
        </FilterBar>
        <Toolbar>
          <BaseButton>Tool</BaseButton>
        </Toolbar>
      </>,
    );
    fireEvent.submit(screen.getByRole("search"));
    expect(onSearch).toHaveBeenCalledWith("bazi");
    expect(screen.getByRole("group", { name: "Filters" })).toBeTruthy();
    expect(screen.getByRole("toolbar", { name: "Toolbar" })).toBeTruthy();
  });

  it("renders reference, glossary, tags, chips, skeletons", () => {
    render(
      <>
        <FooterNote>Disclaimer</FooterNote>
        <GlossaryEntry term="Day Master" definition="Definition" />
        <ReferenceBlock>
          <CitationRow citation="Cite 1" source="Src" />
        </ReferenceBlock>
        <TagGroup>
          <BaseTag>Tag</BaseTag>
        </TagGroup>
        <ChipGroup>
          <BaseChip>Chip</BaseChip>
        </ChipGroup>
        <SkeletonSection />
        <SkeletonMetric />
        <SkeletonParagraph />
      </>,
    );
    expect(screen.getByText("Disclaimer")).toBeTruthy();
    expect(screen.getByText("Day Master")).toBeTruthy();
    expect(screen.getByText("Cite 1")).toBeTruthy();
    expect(screen.getByText("Tag")).toBeTruthy();
    expect(screen.getByText("Chip")).toBeTruthy();
  });
});
