import type { ReactNode } from "react";

import { Badge } from "../../../components/base/Badge";
import { PREVIEW_DESTINY } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Mệnh Cục — cách cục / điều hậu / summary / quality badge slots.
 */
export function DestinyPanel({ preview }: { preview: boolean }): ReactNode {
  return (
    <div className="bte-rw-panel" data-shell="destiny">
      <div className="bte-rw-stat" data-slot="destiny-pattern">
        <span className="bte-rw-label">Cách cục</span>
        <p className="bte-rw-primary">
          <SlotValue preview={preview} value={PREVIEW_DESTINY.pattern} />
        </p>
      </div>
      <div className="bte-rw-stat" data-slot="destiny-climate">
        <span className="bte-rw-label">Điều hậu</span>
        <p className="bte-rw-secondary">
          <SlotValue preview={preview} value={PREVIEW_DESTINY.climate} />
        </p>
      </div>
      <p className="bte-rw-caption" data-slot="destiny-summary">
        <SlotValue preview={preview} value={PREVIEW_DESTINY.summary} />
      </p>
      <div className="bte-rw-inline" data-slot="destiny-quality">
        <span className="bte-rw-label">Đánh giá</span>
        {preview ? (
          <Badge tone="accent">{PREVIEW_DESTINY.quality}</Badge>
        ) : (
          <SlotValue preview={false} />
        )}
      </div>
    </div>
  );
}
