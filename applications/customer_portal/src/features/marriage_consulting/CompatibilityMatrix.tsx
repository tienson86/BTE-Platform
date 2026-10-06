import { useId, useState, type ReactNode } from "react";

import type { MarriageMatrixSectionVm } from "./types";

const STATUS_LABEL: Record<string, string> = {
  supportive: "Hỗ trợ",
  balanced: "Cân bằng",
  mixed: "Hai chiều",
  pressured: "Áp lực",
  reference: "Tham khảo",
  unavailable: "Thiếu dữ liệu",
};

type Props = {
  sections: MarriageMatrixSectionVm[];
  personALabel?: string;
  personBLabel?: string;
  introduction?: string;
};

export function CompatibilityMatrix({
  sections,
  personALabel = "Người Nữ",
  personBLabel = "Người Nam",
  introduction = "Mỗi hàng nêu dữ liệu hai người và quy tắc đối chiếu. Đây là mô hình luận giải Bát Tự minh bạch, không phải bằng chứng khoa học dự đoán hạnh phúc.",
}: Props): ReactNode {
  const id = useId();
  const [activeKey, setActiveKey] = useState(sections[0]?.key || "");
  const active = sections.find((item) => item.key === activeKey) || sections[0];
  if (!active) return null;
  return (
    <section className="mc-matrix" data-testid="compatibility-matrix">
      <div className="mc-matrix__heading">
        <div>
          <h2>Bảng đối chiếu có thể kiểm chứng</h2>
          <p className="muted">{introduction}</p>
        </div>
        <div className="mc-matrix__legend" aria-label="Chú giải trạng thái">
          <span data-status="supportive">Hỗ trợ</span>
          <span data-status="pressured">Áp lực</span>
          <span data-status="reference">Tham khảo</span>
        </div>
      </div>
      <div className="mc-matrix__tabs" role="tablist" aria-label="Nhóm đối chiếu">
        {sections.map((item) => (
          <button
            type="button"
            role="tab"
            id={`${id}-${item.key}`}
            aria-controls={`${id}-panel`}
            aria-selected={item.key === active.key}
            className={item.key === active.key ? "is-active" : ""}
            key={item.key}
            onClick={() => setActiveKey(item.key)}
          >
            {item.title}
          </button>
        ))}
      </div>
      <div className="mc-matrix__panel" role="tabpanel" id={`${id}-panel`} aria-labelledby={`${id}-${active.key}`} data-testid={`matrix-section-${active.key}`}>
        <p className="mc-matrix__description">{active.description}</p>
        <div className="mc-matrix__table-wrap">
          <table className="mc-matrix__table">
            <thead>
              <tr>
                <th>Tiêu chí</th>
                <th>{personALabel}</th>
                <th>{personBLabel}</th>
                <th>Kết quả đối chiếu</th>
                <th>Cơ sở</th>
              </tr>
            </thead>
            <tbody>
              {active.rows.map((row) => (
                <tr key={row.key} data-status={row.available ? row.status : "unavailable"}>
                  <th data-label="Tiêu chí" scope="row">{row.label}</th>
                  <td data-label={personALabel}>{row.personA}</td>
                  <td data-label={personBLabel}>{row.personB}</td>
                  <td data-label="Kết quả">
                    <span className="mc-matrix__status" data-status={row.available ? row.status : "unavailable"}>
                      {STATUS_LABEL[row.available ? row.status : "unavailable"] || row.status}
                    </span>
                    <p>{row.relationship}</p>
                    {row.available && row.scoreEffect !== null ? (
                      <small>
                        Ảnh hưởng kỹ thuật: {row.scoreEffect > 0 ? "+" : ""}{row.scoreEffect}; được giới hạn khi gộp điểm.
                      </small>
                    ) : null}
                  </td>
                  <td data-label="Cơ sở">
                    <p>{row.basis}</p>
                    <small>Độ tin cậy dữ liệu: {Math.round(row.confidence * 100)}%</small>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
