import type { ReactNode } from "react";

import { Badge } from "../../../components/base/Badge";
import type { WorkspacePatternView } from "../adapter/types";
import { PREVIEW_DESTINY } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Mệnh Cục — pattern / temperature slots. No new interpretation copy.
 */
export function DestinyPanel({
  preview,
  model,
}: {
  preview: boolean;
  model?: WorkspacePatternView;
}): ReactNode {
  const bound = Boolean(model) && !preview;
  const quality = preview ? PREVIEW_DESTINY.quality : model?.quality.value;
  return (
    <div className="bte-rw-panel" data-shell="destiny">
      <div className="bte-rw-stat" data-slot="destiny-pattern">
        <span className="bte-rw-label">Cách cục</span>
        <p className="bte-rw-primary">
          <SlotValue
            preview={preview}
            bound={bound}
            value={preview ? PREVIEW_DESTINY.pattern : model?.pattern.value}
          />
        </p>
      </div>
      <div className="bte-rw-stat" data-slot="destiny-climate">
        <span className="bte-rw-label">Điều hậu</span>
        <p className="bte-rw-secondary">
          <SlotValue
            preview={preview}
            bound={bound}
            value={preview ? PREVIEW_DESTINY.climate : model?.climate.value}
          />
        </p>
      </div>
      <p className="bte-rw-caption" data-slot="destiny-summary">
        <SlotValue
          preview={preview}
          bound={bound}
          value={preview ? PREVIEW_DESTINY.summary : model?.summary.value}
        />
      </p>
      <div className="bte-rw-inline" data-slot="destiny-quality">
        <span className="bte-rw-label">Đánh giá</span>
        {quality ? (
          <Badge tone="accent">{quality}</Badge>
        ) : (
          <SlotValue preview={false} />
        )}
      </div>
    </div>
  );
}
