import { PvButton, PvCard } from "./primitives";

export type ReportMode = "reading" | "print" | "presentation" | "sharing";

export function CommercialRail({
  saved,
  onSave,
  onPdf,
  onPrint,
  onShare,
  onKnowledge,
  onPremium,
}: {
  saved: boolean;
  onSave: () => void;
  onPdf: () => void;
  onPrint: () => void;
  onShare: () => void;
  onKnowledge: () => void;
  onPremium: () => void;
}) {
  return (
    <section className="pv-commercial" aria-label="Việc làm tiếp theo với báo cáo">
      <PvCard title={<h2 className="pv-card-title">Giữ lại buổi tư vấn này</h2>}>
        <p className="pv-prose">
          {saved
            ? "Báo cáo đã được lưu trên thiết bị này. Bạn có thể mở lại từ Lịch sử."
            : "Lưu để đọc lại, in thành PDF, hoặc chia sẻ tóm tắt khi bạn sẵn sàng."}
        </p>
        <div className="pv-cta-row">
          <PvButton onClick={onSave} disabled={saved}>
            {saved ? "Đã lưu báo cáo" : "Lưu báo cáo"}
          </PvButton>
          <PvButton variant="secondary" onClick={onPdf}>
            Tải bản PDF
          </PvButton>
          <PvButton variant="secondary" onClick={onPrint}>
            In tư vấn
          </PvButton>
          <PvButton variant="text" onClick={onShare}>
            Chia sẻ
          </PvButton>
        </div>
      </PvCard>
      <PvCard title={<h3 className="pv-card-title">Tiếp tục đọc</h3>}>
        <p className="pv-prose">Bài liên quan: Nhật chủ — không thay thế định hướng vừa đọc.</p>
        <div className="pv-cta-row">
          <PvButton variant="secondary" onClick={onKnowledge}>
            Mở bài liên quan
          </PvButton>
          <PvButton variant="text" onClick={onPremium}>
            Đặt tư vấn chuyên sâu
          </PvButton>
        </div>
      </PvCard>
    </section>
  );
}
