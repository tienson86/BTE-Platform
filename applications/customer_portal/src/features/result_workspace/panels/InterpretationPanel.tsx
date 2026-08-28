import type { ReactNode } from "react";

import { INTERPRETATION_BLOCKS } from "../catalog";
import { PREVIEW_INTERPRETATION } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Luận Giải Tổng Thể — four reasoning blocks for future Interpretation output.
 */
export function InterpretationPanel({ preview }: { preview: boolean }): ReactNode {
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
              <SlotValue preview={preview} value={PREVIEW_INTERPRETATION[block.id]} />
            </p>
          </section>
        ))}
      </div>
    </div>
  );
}
