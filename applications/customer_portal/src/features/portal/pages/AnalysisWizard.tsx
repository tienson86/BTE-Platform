import { PvButton, PvCard, PvInput, PvRadio, PvSelect } from "../components/primitives";
import type { PortalRoute } from "../chrome/routes";

export type WizardDraft = {
  name: string;
  place: string;
  year: string;
  month: string;
  day: string;
  hour: string;
  minute: string;
  gender: string;
  calendar: string;
};

const STEPS = [
  { id: "analyze", label: "Tổng quan" },
  { id: "analyze-birth", label: "Ngày sinh" },
  { id: "analyze-chart", label: "Lá số" },
  { id: "analyze-progress", label: "Tiến trình" },
] as const;

function Stepper({ current }: { current: PortalRoute }) {
  return (
    <ol className="pv-stepper" aria-label="Các bước phân tích">
      {STEPS.map((step, index) => {
        const active = step.id === current;
        const done = STEPS.findIndex((item) => item.id === current) > index;
        return (
          <li key={step.id} data-active={active || undefined} data-done={done || undefined}>
            <span className="pv-stepper__index">{index + 1}</span>
            <span>{step.label}</span>
          </li>
        );
      })}
    </ol>
  );
}

export function NewAnalysisPage({
  onNavigate,
}: {
  onNavigate: (route: PortalRoute) => void;
}) {
  return (
    <section className="pv-page">
      <Stepper current="analyze" />
      <PvCard title={<h2 className="pv-heading">Bắt đầu một buổi tư vấn mới</h2>}>
        <p className="pv-prose">
          Bạn sẽ nhập ngày sinh, xác nhận lá số, rồi chờ tiến trình ngắn. Không cần thuật ngữ kỹ thuật.
        </p>
        <div className="pv-cta-row">
          <PvButton onClick={() => onNavigate("analyze-birth")}>Tiếp tục</PvButton>
          <PvButton variant="text" onClick={() => onNavigate("dashboard")}>
            Quay lại tổng quan
          </PvButton>
        </div>
      </PvCard>
    </section>
  );
}

export function BirthInformationPage({
  draft,
  onChange,
  onNavigate,
}: {
  draft: WizardDraft;
  onChange: (patch: Partial<WizardDraft>) => void;
  onNavigate: (route: PortalRoute) => void;
}) {
  const valid = draft.name.trim().length > 1 && draft.place.trim().length > 1;
  return (
    <section className="pv-page">
      <Stepper current="analyze-birth" />
      <PvCard title={<h2 className="pv-heading">Thông tin ngày sinh</h2>}>
        <p className="pv-hint">Nhập như bạn vẫn kể với chuyên gia: tên, nơi sinh, ngày giờ.</p>
        <div className="pv-form-grid">
          <PvInput label="Họ và tên" value={draft.name} onChange={(event) => onChange({ name: event.target.value })} required />
          <PvInput label="Nơi sinh" value={draft.place} onChange={(event) => onChange({ place: event.target.value })} required />
          <PvInput label="Năm" type="number" value={draft.year} onChange={(event) => onChange({ year: event.target.value })} />
          <PvInput label="Tháng" type="number" value={draft.month} onChange={(event) => onChange({ month: event.target.value })} />
          <PvInput label="Ngày" type="number" value={draft.day} onChange={(event) => onChange({ day: event.target.value })} />
          <PvInput label="Giờ" type="number" value={draft.hour} onChange={(event) => onChange({ hour: event.target.value })} />
          <PvInput label="Phút" type="number" value={draft.minute} onChange={(event) => onChange({ minute: event.target.value })} />
        </div>
        <fieldset className="pv-fieldset">
          <legend>Giới tính</legend>
          <PvRadio name="gender" label="Nam" value="male" checked={draft.gender === "male"} onChange={() => onChange({ gender: "male" })} />
          <PvRadio name="gender" label="Nữ" value="female" checked={draft.gender === "female"} onChange={() => onChange({ gender: "female" })} />
          <PvRadio name="gender" label="Không nêu" value="" checked={draft.gender === ""} onChange={() => onChange({ gender: "" })} />
        </fieldset>
        <div className="pv-cta-row">
          <PvButton disabled={!valid} onClick={() => onNavigate("analyze-chart")}>
            Tiếp tục
          </PvButton>
          <PvButton variant="text" onClick={() => onNavigate("analyze")}>
            Quay lại
          </PvButton>
        </div>
      </PvCard>
    </section>
  );
}

export function ChartInputPage({
  draft,
  onChange,
  onNavigate,
}: {
  draft: WizardDraft;
  onChange: (patch: Partial<WizardDraft>) => void;
  onNavigate: (route: PortalRoute) => void;
}) {
  return (
    <section className="pv-page">
      <Stepper current="analyze-chart" />
      <PvCard title={<h2 className="pv-heading">Thông tin lá số</h2>}>
        <p className="pv-hint">Chỉ cần lịch và múi giờ. Phần còn lại hệ thống sẽ sắp xếp.</p>
        <div className="pv-form-grid">
          <PvSelect label="Lịch" value={draft.calendar} onChange={(event) => onChange({ calendar: event.target.value })}>
            <option value="solar">Dương lịch</option>
            <option value="lunar">Âm lịch</option>
          </PvSelect>
          <PvInput label="Múi giờ" value="Việt Nam (UTC+7)" readOnly />
        </div>
        <div className="pv-cta-row">
          <PvButton onClick={() => onNavigate("analyze-progress")}>Bắt đầu phân tích</PvButton>
          <PvButton variant="text" onClick={() => onNavigate("analyze-birth")}>
            Quay lại
          </PvButton>
        </div>
      </PvCard>
    </section>
  );
}

export function AnalysisProgressPage({
  draft,
  onNavigate,
}: {
  draft: WizardDraft;
  onNavigate: (route: PortalRoute) => void;
}) {
  return (
    <section className="pv-page">
      <Stepper current="analyze-progress" />
      <PvCard title={<h2 className="pv-heading">Đang chuẩn bị tư vấn</h2>}>
        <p className="pv-prose">Đang sắp xếp hồ sơ cho {draft.name || "bạn"}. Bạn có thể mở kết quả khi sẵn sàng.</p>
        <div className="pv-progress" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={72} aria-label="Tiến trình phân tích">
          <span style={{ width: "72%" }} />
        </div>
        <div className="pv-cta-row">
          <PvButton onClick={() => onNavigate("result")}>Xem kết quả</PvButton>
          <PvButton variant="secondary" onClick={() => onNavigate("dashboard")}>
            Về tổng quan
          </PvButton>
        </div>
      </PvCard>
    </section>
  );
}
