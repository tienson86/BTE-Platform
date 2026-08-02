import {
  EmptyState,
  ErrorState,
  LoadingState,
  ReadingProgress,
  SectionDivider,
  SectionHeader,
  UnavailableState,
} from "../components/shared";
import type { AppendixViewModel } from "../view_models/appendix";
import { cx } from "../utils";
import {
  AppendixContainer,
  AppendixSummary,
  CitationSection,
  CreditsSection,
  GlossarySection,
  KnowledgeReferenceSection,
  RuleReferenceSection,
  SectionTransition,
  TerminologySection,
  VersionInformation,
} from "../components/business";

export type AppendixScreenProps = {
  data: AppendixViewModel;
  readingProgress?: number;
  className?: string;
};

/**
 * Appendix Screen — Pack 03 / Pack 06 WP-0010.
 * Reading order is fixed and must not be reordered.
 *
 * Header → Summary → Glossary → Terminology → Knowledge → Rules →
 * Citations → Credits → Version → Transition
 */
export function AppendixScreen({
  data,
  readingProgress,
  className,
}: AppendixScreenProps) {
  if (data.status !== "ready") {
    return (
      <AppendixContainer className={cx(className)}>
        {data.status === "loading" ? (
          <LoadingState title="Loading appendix" />
        ) : null}
        {data.status === "empty" ? (
          <EmptyState title="No appendix available" />
        ) : null}
        {data.status === "unavailable" ? (
          <UnavailableState title="Appendix unavailable" />
        ) : null}
        {data.status === "error" ? (
          <ErrorState
            title="Unable to load appendix"
            description={data.errorMessage}
          />
        ) : null}
      </AppendixContainer>
    );
  }

  const title = data.header?.title ?? "Appendix";

  return (
    <AppendixContainer className={cx("cui-biz-appendix-screen", className)}>
      {typeof readingProgress === "number" ? (
        <ReadingProgress value={readingProgress} />
      ) : null}

      {/* 1. Appendix Header */}
      <SectionHeader title={title} subtitle={data.header?.subtitle} level={2} />
      <SectionDivider />

      {/* Optional summary */}
      {data.summary ? (
        <>
          <AppendixSummary data={data.summary} />
          <SectionDivider />
        </>
      ) : null}

      {/* 2. Glossary */}
      <GlossarySection items={data.glossary} />
      <SectionDivider />

      {/* 3. Terminology */}
      <TerminologySection items={data.terminology} />
      <SectionDivider />

      {/* 4. Knowledge References */}
      <KnowledgeReferenceSection items={data.knowledgeReferences} />
      <SectionDivider />

      {/* 5. Rule References */}
      <RuleReferenceSection items={data.ruleReferences} />
      <SectionDivider />

      {/* Interpretation / Citations */}
      <CitationSection items={data.citations} />
      <SectionDivider />

      {/* 6. Credits */}
      <CreditsSection data={data.credits} />
      <SectionDivider />

      {/* 7. Version Information */}
      <VersionInformation data={data.version} />

      {data.transition ? (
        <>
          <SectionDivider />
          <SectionTransition
            label={data.transition.label}
            href={data.transition.href}
          />
        </>
      ) : null}
    </AppendixContainer>
  );
}
