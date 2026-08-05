import { memo, type ReactNode } from "react";
import type {
  BaZiChartMetadata,
  BaZiProfile,
  BaZiResultLabels,
  PresentationStatus,
} from "./mockData";

export type ContextHeaderProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  profile: BaZiProfile;
  metadata: BaZiChartMetadata;
  errorMessage?: string;
};

/**
 * S00 — Context Header
 * Step 1 (revised): Desktop Layout Skeleton = IA wireframe.
 * Exposes Left / Center / Right regions and information zones.
 * Not a loading skeleton. No product data. No responsive.
 */
export const ContextHeader = memo(function ContextHeader({
  labels,
}: ContextHeaderProps): ReactNode {
  return (
    <header
      id="ngu-canh"
      className="cui-bazi-context"
      aria-label={labels.contextTitle}
      data-section="s00-context"
      data-layout-token="ContextRegion"
      data-skeleton="desktop-wireframe"
    >
      {/* Top Container */}
      <div className="cui-bazi-context__strip">
        <div className="cui-bazi-context__strip-label">S00 · Context Header · Top Container</div>

        <div className="cui-bazi-context__grid">
          {/* LEFT REGION */}
          <section
            className="cui-bazi-context__region cui-bazi-context__region--left"
            aria-label="Left Region"
          >
            <div className="cui-bazi-context__region-label">LEFT</div>
            <div className="cui-bazi-context__zone" data-zone="avatar">
              <div className="cui-bazi-context__zone-label">Avatar</div>
              <div className="cui-bazi-context__slot cui-bazi-context__slot--avatar" />
            </div>
          </section>

          {/* CENTER REGION */}
          <section
            className="cui-bazi-context__region cui-bazi-context__region--center"
            aria-label="Center Region"
          >
            <div className="cui-bazi-context__region-label">CENTER</div>

            <div className="cui-bazi-context__zone" data-zone="primary">
              <div className="cui-bazi-context__zone-label">Primary · Identity</div>
              <div className="cui-bazi-context__slot">Tên hồ sơ</div>
              <div className="cui-bazi-context__slot">Giới tính</div>
              <div className="cui-bazi-context__slot cui-bazi-context__slot--wide">
                Ngày giờ sinh · Địa điểm
              </div>
            </div>

            <div className="cui-bazi-context__divider" role="separator" />

            <div className="cui-bazi-context__zone" data-zone="metadata">
              <div className="cui-bazi-context__zone-label">Secondary · Metadata</div>
              <div className="cui-bazi-context__slot">Mã lá số</div>
              <div className="cui-bazi-context__slot">Phiên bản</div>
              <div className="cui-bazi-context__slot">Thời điểm phân tích</div>
            </div>
          </section>

          {/* RIGHT REGION */}
          <section
            className="cui-bazi-context__region cui-bazi-context__region--right"
            aria-label="Right Region"
          >
            <div className="cui-bazi-context__region-label">RIGHT</div>

            <div className="cui-bazi-context__zone" data-zone="status">
              <div className="cui-bazi-context__zone-label">Status</div>
              <div className="cui-bazi-context__slot">Trạng thái</div>
            </div>

            <div className="cui-bazi-context__zone" data-zone="actions">
              <div className="cui-bazi-context__zone-label">Supporting · Actions</div>
              <div className="cui-bazi-context__slot">Chi tiết hồ sơ</div>
              <div className="cui-bazi-context__slot">Phân tích lại</div>
            </div>
          </section>
        </div>
      </div>
    </header>
  );
});
