import type { HTMLAttributes, ReactNode } from "react";
import { BaseStack, BaseText } from "../base";
import { cx } from "../../utils";

export type GlossaryEntryProps = HTMLAttributes<HTMLElement> & {
  term: ReactNode;
  definition: ReactNode;
};

/** Shared glossary term/definition. */
export function GlossaryEntry({
  term,
  definition,
  className,
  ...rest
}: GlossaryEntryProps) {
  return (
    <BaseStack
      as="section"
      gap="inline"
      className={cx("cui-shared-glossary-entry", className)}
      {...rest}
    >
      <BaseText variant="subsection">{term}</BaseText>
      <BaseText variant="body" tone="secondary">
        {definition}
      </BaseText>
    </BaseStack>
  );
}
