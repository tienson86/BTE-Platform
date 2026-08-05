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
  IconDrop,
  IconFire,
  IconGrid,
  IconHome,
  IconLeaf,
  IconPalette,
  IconPersonMark,
  IconScale,
  IconSpark,
  IconTarget,
  IconUser,
  IconYinYang,
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

function ElementDonut(): ReactNode {
  const legend = d.s04.legend;
  const r = 42;
  const c = 2 * Math.PI * r;
  let offset = 0;
  const segments = legend.map((item) => {
    const len = (item.pct / 100) * c;
    const seg = { ...item, len, offset };
    offset += len;
    return seg;
  });

  return (
    <div className="cd-s04__chart-wrap">
      <svg width="120" height="120" viewBox="0 0 120 120" aria-hidden="true">
        <g transform="translate(60,60) rotate(-90)">
          {segments.map((seg) => (
            <circle
              key={seg.name}
              r={r}
              cx="0"
              cy="0"
              fill="transparent"
              stroke={seg.color}
              strokeWidth="16"
              strokeDasharray={`${seg.len} ${c - seg.len}`}
              strokeDashoffset={-seg.offset}
            />
          ))}
        </g>
      </svg>
      <div className="cd-s04__chart-center">
        <span>{d.s04.totalLabel}</span>
        <strong>{d.s04.totalValue}</strong>
      </div>
    </div>
  );
}

export function S00ContextHeader(): ReactNode {
  const s = d.s00;
  return (
    <section className="cd-s00" id="tom-tat" aria-labelledby="cd-s00-title">
      <h2 id="cd-s00-title" className="cd-section-title">
        {s.title}
      </h2>
      <div className="cd-card">
        <div className="cd-s00__body">
          <div className="cd-s00__col">
            <div className="cd-label">{s.profile.label}</div>
            <div className="cd-s00__profile">
              <div className="cd-s00__avatar">
                <IconUser size={28} />
              </div>
              <div>
                <p className="cd-s00__name">
                  {s.profile.name}
                  <span className="cd-s00__gender">{s.profile.genderSymbol}</span>
                </p>
                <p className="cd-s00__meta">{s.profile.meta}</p>
                <a className="cd-link" href="#ho-so">
                  {s.profile.profileLink}
                </a>
              </div>
            </div>
          </div>

          <div className="cd-s00__col">
            <div className="cd-label">{s.birth.label}</div>
            <div className="cd-s00__birth-row">
              <IconCalendar />
              <strong>{s.birth.date}</strong>
              <span className="cd-s00__lunar">{s.birth.lunar}</span>
            </div>
            <div className="cd-s00__birth-row">
              <IconClock />
              <strong>{s.birth.time}</strong>
            </div>
          </div>

          <div className="cd-s00__col">
            <div className="cd-label">{s.chartId.label}</div>
            <div className="cd-s00__chart-id">
              <span>{s.chartId.value}</span>
              <IconCopy />
            </div>
          </div>

          <div className="cd-s00__col">
            <div className="cd-label">{s.version.label}</div>
            <div className="cd-s00__version-value">{s.version.value}</div>
            <div className="cd-s00__version-sys">{s.version.system}</div>
          </div>

          <div className="cd-s00__col">
            <div className="cd-label">{s.analyzedAt.label}</div>
            <div className="cd-s00__version-value" style={{ fontSize: 13 }}>
              {s.analyzedAt.value}
            </div>
            <div className="cd-s00__relative">{s.analyzedAt.relative}</div>
          </div>

          <div className="cd-s00__col">
            <div className="cd-label">{s.status.label}</div>
            <div className="cd-s00__status">
              <span>{s.status.value}</span>
              <span className="cd-s00__dot" />
            </div>
            <a className="cd-link" href="#chia-se" style={{ marginTop: 8 }}>
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
  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s01-title">
      <h2 id="cd-s01-title" className="cd-section-title">
        {s.title}
      </h2>
      <div className="cd-s01">
        <div>
          <h3 className="cd-s01__sub">{s.identityTitle}</h3>
          <div className="cd-s01__day">
            <div className="cd-s01__fire">
              <IconFire size={22} />
            </div>
            <div>
              <div className="cd-s01__day-label">{s.dayMaster.label}</div>
              <div className="cd-s01__day-value">{s.dayMaster.value}</div>
              <div className="cd-s01__day-sub">{s.dayMaster.subtype}</div>
              <div className="cd-s01__tags">
                {s.dayMaster.tags.map((tag) => (
                  <span key={tag.text} className={`cd-tag cd-tag--${tag.tone}`}>
                    {tag.text}
                  </span>
                ))}
              </div>
            </div>
          </div>
          <div style={{ marginTop: 10 }}>
            <div className="cd-label" style={{ marginBottom: 4 }}>
              {s.conditions.title}
            </div>
            {s.conditions.rows.map((row) => (
              <div key={row.label} className="cd-s01__cond-row">
                <div className="cd-s01__cond-left">
                  <strong>{row.label}:</strong>
                  {row.value}
                </div>
                <span className={`cd-tag cd-tag--${row.tone}`}>{row.tag}</span>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h3 className="cd-s01__sub">{s.decisionTitle}</h3>
          <div className="cd-s01__decisions">
            {s.decisions.map((item) => (
              <div key={item.question} className="cd-s01__decision">
                <div className={`cd-s01__decision-icon cd-s01__decision-icon--${item.icon}`}>
                  {item.icon === "target" && <IconTarget />}
                  {item.icon === "bulb" && <IconBulb />}
                  {item.icon === "compass" && <IconCompass />}
                </div>
                <div>
                  <p className="cd-s01__q">{item.question}</p>
                  <p className="cd-s01__a">{item.answer}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="cd-s01__cta">
          <button type="button" className="cd-btn-primary">
            {s.cta}
          </button>
        </div>
      </div>
    </section>
  );
}

export function S02OverviewActions(): ReactNode {
  const s = d.s02;
  const iconMap = {
    fire: <IconFire color="#c62828" />,
    yinyang: <IconYinYang color="#1565c0" />,
    scale: <IconScale color="#6a1b9a" />,
    drop: <IconDrop color="#1565c0" />,
    spark: <IconSpark color="#f9a825" />,
    leaf: <IconLeaf color="#2e7d32" />,
  } as const;

  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s02-title">
      <h2 id="cd-s02-title" className="cd-section-title">
        {s.title}
      </h2>
      <h3 className="cd-s01__sub">{s.subtitle}</h3>
      <div className="cd-s02__grid">
        {s.items.map((item) => (
          <div key={item.label} className="cd-s02__item">
            <div className="cd-s02__item-icon">{iconMap[item.icon]}</div>
            <div className="cd-s02__item-label">{item.label}</div>
            <div className={`cd-s02__item-value cd-s02__item-value--${item.color}`}>
              {item.value}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

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

export function S03FourPillars(): ReactNode {
  const s = d.s03;
  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s03-title">
      <h2 id="cd-s03-title" className="cd-section-title">
        {s.title}
      </h2>
      <div className="cd-s03__pillars">
        {s.pillars.map((p) => (
          <article
            key={p.title}
            className={p.highlight ? "cd-s03__pillar cd-s03__pillar--hl" : "cd-s03__pillar"}
          >
            <div className="cd-s03__pillar-title">{p.title}</div>
            <div className={`cd-s03__han cd-s03__han--${p.stem.tone}`}>{p.stem.han}</div>
            <div className="cd-s03__viet">{p.stem.viet}</div>
            <div className="cd-s03__el">{p.stem.element}</div>
            <div className="cd-s03__divider" />
            <div className={`cd-s03__han cd-s03__han--${p.branch.tone}`}>{p.branch.han}</div>
            <div className="cd-s03__viet">{p.branch.viet}</div>
            <div className="cd-s03__el">{p.branch.element}</div>
            <div className="cd-s03__stamp">{p.stamp}</div>
          </article>
        ))}
      </div>
    </section>
  );
}

export function S04ElementBalance(): ReactNode {
  const s = d.s04;
  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s04-title">
      <h2 id="cd-s04-title" className="cd-section-title">
        {s.title}
      </h2>
      <div className="cd-s04__body">
        <ElementDonut />
        <ul className="cd-s04__legend">
          {s.legend.map((item) => (
            <li key={item.name}>
              <span className="cd-s04__dot" style={{ background: item.color }} />
              <span>{item.name}</span>
              <span className="cd-s04__pct">{item.pct}%</span>
            </li>
          ))}
        </ul>
      </div>
      <p className="cd-s04__summary">{s.summary}</p>
    </section>
  );
}

export function S05Strength(): ReactNode {
  const s = d.s05;
  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s05-title">
      <h2 id="cd-s05-title" className="cd-section-title">
        {s.title}
      </h2>
      <div className="cd-s05__body">
        <div>
          <div className="cd-label">{s.scoreLabel}</div>
          <div className="cd-s05__score">{s.score}</div>
          <div className="cd-s05__status">{s.status}</div>
          <div className="cd-s05__bar" aria-hidden="true">
            <span style={{ width: `${s.percent}%` }} />
          </div>
        </div>
        <div>
          <div className="cd-label">{s.evidenceTitle}</div>
          <ul className="cd-s05__evidence">
            {s.evidence.map((e) => (
              <li key={e}>{e}</li>
            ))}
          </ul>
        </div>
      </div>
      <div className="cd-s05__footer">
        <a className="cd-link" href="#s05-detail">
          {s.link}
        </a>
      </div>
    </section>
  );
}

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

export function S06TenGods(): ReactNode {
  const s = d.s06;
  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s06-title">
      <h2 id="cd-s06-title" className="cd-section-title">
        {s.title}
      </h2>
      <div className="cd-s06__grid">
        {s.gods.map((g) => (
          <div key={g.name} className="cd-s06__god">
            <div className="cd-s06__god-icon" style={{ background: g.color }}>
              •
            </div>
            <div className="cd-s06__god-name">{g.name}</div>
            <div
              className={
                g.highlight ? "cd-s06__god-value cd-s06__god-value--hl" : "cd-s06__god-value"
              }
            >
              {g.value}
            </div>
          </div>
        ))}
      </div>
      <div className="cd-s06__footer">
        <a className="cd-link" href="#s06-detail">
          {s.link}
        </a>
      </div>
    </section>
  );
}

export function S07ShenSha(): ReactNode {
  const s = d.s07;
  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s07-title">
      <h2 id="cd-s07-title" className="cd-section-title">
        {s.title}
      </h2>
      <div className="cd-s07__cats">
        {s.categories.map((cat) => (
          <div key={cat.name} className="cd-s07__cat">
            <div className="cd-s07__cat-name">{cat.name}</div>
            {cat.items.map((item) => (
              <div key={item} className="cd-s07__cat-item">
                {item}
              </div>
            ))}
          </div>
        ))}
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
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s08-title">
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
