import type { ReactNode } from "react";
import { CANONICAL_DESKTOP_MOCK } from "../mockData";
import {
  IconBulb,
  IconCalendar,
  IconClock,
  IconCompass,
  IconCopy,
  IconDoc,
  IconFire,
  IconTarget,
  IconUser,
} from "../icons";

const d = CANONICAL_DESKTOP_MOCK;

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

export { S09CungPhi, S09FengShuiGuidance } from "./S09FengShuiGuidance";

export { S03FourPillars } from "./S03FourPillars";

export { S04ElementBalance } from "./S04ElementBalance";

export { S05ChartStrength, S05Strength } from "./S05ChartStrength";

export { S10BoneWeightFortune, S10CanXuong } from "./S10BoneWeightFortune";

export { S06TenGods } from "./S06TenGods";

export { S07ShenSha } from "./S07ShenSha";

export { S08Interpretation } from "./S08Interpretation";

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
