/**
 * S03 — TỨ TRỤ - BÁT TỰ
 * Isolated rebuild from CANONICAL_PORTAL_UI_DESKTOP_V1.png
 * + knowledge/ui_master/master_sections/S03_FOUR_PILLARS/
 */

import type { ReactNode } from "react";
import { ModuleHeader } from "../ModuleHeader";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

type Tone = "fire" | "water" | "wood" | "metal" | "earth";

type Glyph = {
  han: string;
  viet: string;
  element: string;
  tone: string;
};

/**
 * Resolve ngũ hành tone class for stem/branch glyphs.
 */
function toneClass(tone: string): Tone {
  if (
    tone === "fire" ||
    tone === "water" ||
    tone === "wood" ||
    tone === "metal" ||
    tone === "earth"
  ) {
    return tone;
  }
  return "metal";
}

/**
 * Stem or branch glyph block — Han → Viet → Element, centered.
 */
function GlyphBlock({ glyph }: { glyph: Glyph }): ReactNode {
  const tone = toneClass(glyph.tone);
  return (
    <div className="cd-s03__glyph">
      <div className={`cd-s03__han cd-s03__tone--${tone}`}>{glyph.han}</div>
      <div className={`cd-s03__viet cd-s03__tone--${tone}`}>{glyph.viet}</div>
      <div className={`cd-s03__el cd-s03__tone--${tone}`}>{glyph.element}</div>
    </div>
  );
}

/**
 * S03 Four Pillars — outer card + denser pillar columns; Day pillar highlighted.
 */
export function S03FourPillars(): ReactNode {
  const data = useCanonicalDesktop().s03;
  return (
    <section className="cd-s03" aria-labelledby="cd-s03-title">
      <div className="cd-s03__card">
        <ModuleHeader id="cd-s03-title">{data.title}</ModuleHeader>
        <div className="cd-s03__grid">
          {data.pillars.map((pillar) => {
            const isMaster = pillar.highlight;
            const headerLabel = isMaster
              ? pillar.title.replace(/\s*\(.*\)\s*$/, "").trim()
              : pillar.title;
            const aria = isMaster
              ? `${headerLabel}, Nhật Chủ, ${pillar.stem.viet} ${pillar.branch.viet}`
              : `${headerLabel}, ${pillar.stem.viet} ${pillar.branch.viet}`;

            return (
              <article
                key={pillar.title}
                className={
                  isMaster ? "cd-s03__pillar cd-s03__pillar--master" : "cd-s03__pillar"
                }
                aria-label={aria}
                tabIndex={0}
              >
                <header className="cd-s03__header">
                  <div className="cd-s03__pillar-name">{headerLabel}</div>
                  {isMaster ? (
                    <div className="cd-s03__master-tag">NHẬT CHỦ</div>
                  ) : null}
                </header>

                <GlyphBlock glyph={pillar.stem} />
                <GlyphBlock glyph={pillar.branch} />

                <footer className="cd-s03__footer">{pillar.stamp}</footer>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}
