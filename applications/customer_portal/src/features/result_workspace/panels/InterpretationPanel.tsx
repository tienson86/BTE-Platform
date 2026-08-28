import type { ReactNode } from "react";

import type { WorkspaceInterpretationView } from "../adapter/types";
import { INTERPRETATION_BLOCKS } from "../catalog";
import { PREVIEW_INTERPRETATION } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Luận Giải Tổng Thể — PACK 04 / narrative sections mapped to four blocks.
 */
export function InterpretationPanel({
  preview,
  model,
}: {
  preview: boolean;
  model?: WorkspaceInterpretationView;
}): ReactNode {
  const bound = Boolean(model) && !preview;
  const values = {
    observe: preview ? PREVIEW_INTERPRETATION.observe : model?.observe.value,
    reason: preview ? PREVIEW_INTERPRETATION.reason : model?.reason.value,
    impact: preview ? PREVIEW_INTERPRETATION.impact : model?.impact.value,
    advice: preview ? PREVIEW_INTERPRETATION.advice : model?.advice.value,
  } as const;
  return (
    <div className="bte-rw-panel" data-shell="interpretation">
      <div className="bte-rw-blocks">
        {INTERPRETATION_BLOCKS.map((block) => (
          <section
            key={block.id}
            className="bte-rw-block"
            data-slot="reason-block"
            data-block={block.id}
          >
            <h3 className="bte-rw-label">{block.title}</h3>
            <p className="bte-rw-caption">
              <SlotValue preview={preview} bound={bound} value={values[block.id]} />
            </p>
          </section>
        ))}
      </div>
    </div>
  );
}
