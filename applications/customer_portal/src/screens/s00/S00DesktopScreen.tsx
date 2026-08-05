/**
 * S00 Desktop screen — blank-page rebuild from CANONICAL_PORTAL_UI.png.
 * Isolated from legacy AppLayout / BaZiResultScreen.
 */

import type { ReactNode } from "react";
import { S00ContextHeader } from "./S00ContextHeader";
import "../../styles/s00-canonical.css";

const TOC = [
  { id: "tom-tat", label: "Tóm tắt", active: true },
  { id: "bat-tu", label: "Bát Tự", active: false },
  { id: "bieu-do", label: "Biểu đồ", active: false },
  { id: "phan-tich", label: "Phân tích", active: false },
  { id: "luan-giai", label: "Luận giải", active: false },
  { id: "kien-thuc", label: "Kiến thức", active: false },
] as const;

/**
 * Desktop-only page framing S00 against canonical shell proportions.
 * Sidebar + content chrome exist so the screenshot matches CANONICAL_PORTAL_UI.png architecture.
 * S01+ business sections are not implemented — content area shows only layout context under S00.
 */
export function S00DesktopScreen(): ReactNode {
  return (
    <div className="s00-page">
      <S00ContextHeader />

      <div className="s00-body">
        <aside className="s00-toc" aria-label="Mục lục">
          <div className="s00-toc__title">MỤC LỤC</div>
          <ul className="s00-toc__list">
            {TOC.map((item) => (
              <li key={item.id}>
                <a
                  href={`#${item.id}`}
                  className={
                    item.active ? "s00-toc__item s00-toc__item--active" : "s00-toc__item"
                  }
                >
                  <span className="s00-toc__icon" aria-hidden="true" />
                  <span>{item.label}</span>
                </a>
              </li>
            ))}
          </ul>
          <div className="s00-toc__footer">
            <div className="s00-toc__theme">
              <span className="s00-toc__theme-label">Chế độ giao diện</span>
              <span className="s00-toc__theme-value">Sáng</span>
            </div>
            <div className="s00-toc__version">BTE Platform v1.0.0</div>
          </div>
        </aside>

        <main className="s00-main" id="tom-tat">
          {/* Layout context only — mirrors canonical first-fold proportions under S00.
              Not an S01 implementation. */}
          <h1 className="s00-main__eyebrow">TÓM TẮT ĐIỀU HÀNH</h1>
          <div className="s00-main__row s00-main__row--4">
            <article className="s00-card">
              <div className="s00-card__icon s00-card__icon--blue" />
              <div className="s00-card__body">
                <div className="s00-card__label">NHẬT CHỦ</div>
                <div className="s00-card__value s00-card__value--blue">Bính</div>
                <div className="s00-card__hint">Hỏa • Dương</div>
              </div>
            </article>
            <article className="s00-card">
              <div className="s00-card__icon s00-card__icon--red" />
              <div className="s00-card__body">
                <div className="s00-card__label">NGŨ HÀNH NHẬT CHỦ</div>
                <div className="s00-card__value s00-card__value--red">Hỏa</div>
                <div className="s00-card__hint">Dương Hỏa</div>
              </div>
            </article>
            <article className="s00-card">
              <div className="s00-card__icon s00-card__icon--dark" />
              <div className="s00-card__body">
                <div className="s00-card__label">ÂM DƯƠNG</div>
                <div className="s00-card__value">Dương</div>
                <div className="s00-card__hint">Dương Nam</div>
              </div>
            </article>
            <article className="s00-card">
              <div className="s00-card__icon s00-card__icon--green" />
              <div className="s00-card__body">
                <div className="s00-card__label">CÂN XƯƠNG ĐOÁN MỆNH</div>
                <div className="s00-card__value s00-card__value--green">4 lượng 8 chỉ</div>
                <div className="s00-card__hint">Thượng cách</div>
                <div className="s00-card__stars" aria-hidden="true">
                  ★★★★★
                </div>
              </div>
            </article>
          </div>

          <div className="s00-main__row s00-main__row--4 s00-main__row--pillars">
            {["NĂM", "THÁNG", "NGÀY", "GIỜ"].map((title) => (
              <article key={title} className="s00-pillar">
                <div className="s00-pillar__title">{title}</div>
                <div className="s00-pillar__rows">
                  {["Thiên Can", "Địa Chi", "Tàng Can", "Nạp Âm", "Trường Sinh"].map((row) => (
                    <div key={row} className="s00-pillar__row">
                      <span>{row}</span>
                      <span className="s00-pillar__val">—</span>
                    </div>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
