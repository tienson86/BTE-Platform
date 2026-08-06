import type { ReactNode } from "react";
import { CANONICAL_DESKTOP_MOCK } from "../mockData";
import {
  IconBriefcase,
  IconBulb,
  IconCalendar,
  IconClock,
  IconCompass,
  IconCopy,
  IconDoc,
  IconFire,
  IconGrid,
  IconHome,
  IconPalette,
  IconPersonMark,
  IconTarget,
  IconUser,
} from "../icons";

const d = CANONICAL_DESKTOP_MOCK;

function BaguaDiagram({ center, number }: { center: string; number: string }): ReactNode {
  return (
    <svg className="cd-s09__bagua" viewBox="0 0 100 100" aria-hidden="true">
      <polygon
        points="50,4 88,22 96,62 70,94 30,94 4,62 12,22"
        fill="#a60000"
        stroke="#7a0000"
        strokeWidth="2"
      />
      {[0, 45, 90, 135, 180, 225, 270, 315].map((deg) => {
        const rad = ((deg - 90) * Math.PI) / 180;
        const x = 50 + Math.cos(rad) * 34;
        const y = 50 + Math.sin(rad) * 34;
        return (
          <rect
            key={deg}
            x={x - 5}
            y={y - 1.5}
            width="10"
            height="3"
            fill="#f5dfa0"
            transform={`rotate(${deg} ${x} ${y})`}
          />
        );
      })}
      <circle cx="50" cy="50" r="22" fill="#fff" />
      <text x="50" y="48" textAnchor="middle" fontSize="11" fontWeight="700" fill="#a60000">
        {center}
      </text>
      <text x="50" y="62" textAnchor="middle" fontSize="14" fontWeight="700" fill="#a60000">
        {number}
      </text>
    </svg>
  );
}

export function S00ContextHeader(): ReactNode {
  const s = d.s00;
  const timeMatch = /^(\d{1,2}:\d{2})\s*(.*)$/.exec(s.birth.time);
  const timePrimary = timeMatch?.[1] ?? s.birth.time;
  const timeSecondary = timeMatch?.[2] ?? "";

  return (
    <section className="cd-s00" id="tom-tat" aria-labelledby="cd-s00-title">
      <h2 id="cd-s00-title" className="cd-s00__title">
        {s.title}
      </h2>
      <div className="cd-s00__card">
        <div className="cd-s00__body">
          <div className="cd-s00__col cd-s00__col--profile">
            <div className="cd-s00__label">{s.profile.label}</div>
            <div className="cd-s00__profile">
              <div className="cd-s00__avatar" aria-hidden="true">
                <IconUser size={26} />
              </div>
              <div className="cd-s00__profile-text">
                <p className="cd-s00__name">
                  {s.profile.name}
                  <span className="cd-s00__gender">{s.profile.genderSymbol}</span>
                </p>
                <p className="cd-s00__meta">{s.profile.meta}</p>
                <a className="cd-s00__link" href="#ho-so">
                  {s.profile.profileLink}
                </a>
              </div>
            </div>
          </div>

          <div className="cd-s00__col">
            <div className="cd-s00__label">{s.birth.label}</div>
            <div className="cd-s00__birth-row">
              <IconCalendar size={14} color="#8b929a" />
              <strong className="cd-s00__primary">{s.birth.date}</strong>
              <span className="cd-s00__secondary">{s.birth.lunar}</span>
            </div>
            <div className="cd-s00__birth-row">
              <IconClock size={14} color="#8b929a" />
              <strong className="cd-s00__primary">{timePrimary}</strong>
              {timeSecondary ? (
                <span className="cd-s00__secondary">{timeSecondary}</span>
              ) : null}
            </div>
          </div>

          <div className="cd-s00__col">
            <div className="cd-s00__label">{s.chartId.label}</div>
            <div className="cd-s00__chart-id">
              <span>{s.chartId.value}</span>
              <IconCopy size={13} />
            </div>
          </div>

          <div className="cd-s00__col">
            <div className="cd-s00__label">{s.version.label}</div>
            <div className="cd-s00__primary cd-s00__primary--lg">{s.version.value}</div>
            <div className="cd-s00__secondary">{s.version.system}</div>
          </div>

          <div className="cd-s00__col">
            <div className="cd-s00__label">{s.analyzedAt.label}</div>
            <div className="cd-s00__primary">{s.analyzedAt.value}</div>
            <div className="cd-s00__secondary">{s.analyzedAt.relative}</div>
          </div>

          <div className="cd-s00__col cd-s00__col--status">
            <div className="cd-s00__label">{s.status.label}</div>
            <div className="cd-s00__status">
              <span>{s.status.value}</span>
              <span className="cd-s00__dot" aria-hidden="true" />
            </div>
            <a className="cd-s00__link" href="#chia-se">
              {s.status.shareLink}
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

export function S01IdentityDecision(): ReactNode {
  const s = d.s01;
  const element = s.dayMaster.value.includes(" ")
    ? s.dayMaster.value.split(" ").slice(1).join(" ")
    : s.dayMaster.value;
  const yinYang = s.dayMaster.subtype.replace(element, "").trim() || s.dayMaster.subtype;
  const strengthBadge = s.dayMaster.tags[0];
  const personalityBadge = s.dayMaster.tags[1];

  return (
    <section className="cd-s01" aria-labelledby="cd-s01-title">
      <h2 id="cd-s01-title" className="cd-s01__title">
        {s.title}
      </h2>
      <div className="cd-s01__card">
        <div className="cd-s01__cols">
          {/* LEFT 60% — Identity + Conditions */}
          <div className="cd-s01__col cd-s01__col--left">
            <div className="cd-s01__block">
              <h3 className="cd-s01__block-title">{s.identityTitle}</h3>
              <div className="cd-s01__identity">
                <div className="cd-s01__identity-icon" aria-hidden="true">
                  <IconFire size={22} />
                </div>
                <div className="cd-s01__identity-body">
                  <div className="cd-s01__identity-label">{s.dayMaster.label}</div>
                  <div className="cd-s01__identity-name">{s.dayMaster.value}</div>
                  <div className="cd-s01__identity-meta">
                    <span>
                      <em>Ngũ hành</em> {element}
                    </span>
                    <span className="cd-s01__identity-dot" aria-hidden="true">
                      ·
                    </span>
                    <span>
                      <em>Âm dương</em> {yinYang}
                    </span>
                  </div>
                  <div className="cd-s01__badges">
                    {strengthBadge ? (
                      <span className={`cd-s01__badge cd-s01__badge--${strengthBadge.tone}`}>
                        {strengthBadge.text}
                      </span>
                    ) : null}
                    {personalityBadge ? (
                      <span className={`cd-s01__badge cd-s01__badge--${personalityBadge.tone}`}>
                        {personalityBadge.text.replace(/^Tính cách:\s*/i, "Tính cách: ")}
                      </span>
                    ) : null}
                  </div>
                </div>
              </div>
            </div>

            <div className="cd-s01__block">
              <h3 className="cd-s01__block-title">{s.conditions.title}</h3>
              <div className="cd-s01__conditions">
                {s.conditions.rows.map((row) => (
                  <div key={row.label} className="cd-s01__cond-row">
                    <div className="cd-s01__cond-text">
                      <span className="cd-s01__cond-label">{row.label}</span>
                      <span className="cd-s01__cond-value">{row.value}</span>
                    </div>
                    <span
                      className={`cd-s01__badge cd-s01__badge--fixed cd-s01__badge--${row.tone}`}
                    >
                      {row.tag}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* RIGHT 40% — Guidance + CTA */}
          <div className="cd-s01__col cd-s01__col--right">
            <div className="cd-s01__block cd-s01__block--guidance">
              <h3 className="cd-s01__block-title">{s.decisionTitle}</h3>
              <div className="cd-s01__guidance">
                {s.decisions.map((item) => (
                  <div key={item.question} className="cd-s01__guide">
                    <div className={`cd-s01__guide-icon cd-s01__guide-icon--${item.icon}`}>
                      {item.icon === "target" && <IconTarget size={15} />}
                      {item.icon === "bulb" && <IconBulb size={15} />}
                      {item.icon === "compass" && <IconCompass size={15} />}
                    </div>
                    <div className="cd-s01__guide-body">
                      <div className="cd-s01__guide-q">{item.question}</div>
                      <p className="cd-s01__guide-a">{item.answer}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <button type="button" className="cd-s01__cta">
              {s.cta}
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

export { S02OverviewActions } from "./S02OverviewActions";

export function S09CungPhi(): ReactNode {
  const s = d.s09;
  const icons = {
    home: <IconHome size={18} color="#fff" />,
    briefcase: <IconBriefcase />,
    compass: <IconCompass size={18} color="#fff" />,
    palette: <IconPalette />,
    grid: <IconGrid />,
  } as const;

  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s09-title">
      <h2 id="cd-s09-title" className="cd-section-title">
        {s.title}
      </h2>
      <div className="cd-s09__quai">
        <BaguaDiagram center={s.quai.center} number={s.quai.number} />
        <ul className="cd-s09__bullets">
          {s.quai.bullets.map((b) => (
            <li key={b}>{b}</li>
          ))}
        </ul>
      </div>
      <h3 className="cd-s09__nhom-title">{s.nhomTrachTitle}</h3>
      <div className="cd-s09__icons">
        {s.nhomTrach.map((item) => (
          <div key={item.label} className="cd-s09__icon-btn">
            <div className={`cd-s09__icon-tile cd-s09__icon-tile--${item.color}`}>
              {icons[item.icon]}
            </div>
            <span className="cd-s09__icon-label">{item.label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

export { S03FourPillars } from "./S03FourPillars";

export { S04ElementBalance } from "./S04ElementBalance";

export { S05ChartStrength, S05Strength } from "./S05ChartStrength";

export function S10CanXuong(): ReactNode {
  const s = d.s10;
  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s10-title">
      <h2 id="cd-s10-title" className="cd-section-title">
        {s.title}
      </h2>
      <div className="cd-s10__body">
        <div>
          <div className="cd-label">{s.resultLabel}</div>
          <div className="cd-s10__result">{s.result}</div>
          <div className="cd-s10__grade">{s.grade}</div>
          <div className="cd-s10__stars" aria-label={`${s.stars} sao`}>
            {"★".repeat(s.stars)}
          </div>
        </div>
        <ul className="cd-s10__bullets">
          {s.bullets.map((b) => (
            <li key={b}>{b}</li>
          ))}
        </ul>
      </div>
      <div className="cd-s10__footer">
        <a className="cd-link" href="#s10-detail">
          {s.link}
        </a>
      </div>
    </section>
  );
}

export { S06TenGods } from "./S06TenGods";

export function S07ShenSha(): ReactNode {
  const s = d.s07;
  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s07-title">
      <h2 id="cd-s07-title" className="cd-section-title">
        {s.title}
      </h2>
      <div className="cd-s07__cats">
        {s.categories.map((cat) => {
          const tone =
            cat.name === "Hung tinh"
              ? "cd-s07__cat cd-s07__cat--hung"
              : cat.name === "Đặc biệt"
                ? "cd-s07__cat cd-s07__cat--dacbiet"
                : "cd-s07__cat cd-s07__cat--cat";
          return (
            <div key={cat.name} className={tone}>
              <div className="cd-s07__cat-name">{cat.name}</div>
              {cat.items.map((item) => (
                <div key={item} className="cd-s07__cat-item">
                  {item}
                </div>
              ))}
            </div>
          );
        })}
      </div>
      <div className="cd-s07__footer">
        <a className="cd-link" href="#s07-detail">
          {s.link}
        </a>
      </div>
    </section>
  );
}

export function S08Interpretation(): ReactNode {
  const s = d.s08;
  return (
    <section className="cd-card cd-card--fill cd-s08" aria-labelledby="cd-s08-title">
      <h2 id="cd-s08-title" className="cd-section-title">
        {s.title}
      </h2>
      <div className="cd-s08__head">
        <div className="cd-s08__icon">
          <IconPersonMark size={18} />
        </div>
        <h3 className="cd-s08__heading">{s.heading}</h3>
      </div>
      <p className="cd-s08__body">{s.body}</p>
      <div className="cd-s08__footer">
        <button type="button" className="cd-btn-primary cd-s08__cta">
          {s.cta}
        </button>
      </div>
    </section>
  );
}

export function S11LearningPanel(): ReactNode {
  const s = d.s11;
  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s11-title">
      <h2 id="cd-s11-title" className="cd-section-title">
        {s.title}
      </h2>
      <ul className="cd-s11__list">
        {s.items.map((item) => (
          <li key={item.label} className="cd-s11__item">
            <span className="cd-s11__item-icon">
              <IconDoc />
            </span>
            <span>{item.label}</span>
            <span className="cd-s11__item-value">{item.value}</span>
          </li>
        ))}
      </ul>
      <div className="cd-s11__footer">
        <a className="cd-link" href="#s11-open">
          {s.link}
        </a>
      </div>
    </section>
  );
}
