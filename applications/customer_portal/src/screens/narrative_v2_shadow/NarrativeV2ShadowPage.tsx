/**
 * Narrative V2 — Shadow Review surface.
 * Diagnostic only. Does not replace Pack05 production /result.
 */

import type { ReactNode } from "react";
import type { AnalysisDataDto } from "../../models";
import {
  adaptNarrativeV2Presentation,
  adaptProductionNarrativeSnippet,
  structuredInterpretationEntries,
  type NarrativeV2ActionView,
  type NarrativeV2OverviewView,
  type NarrativeV2PresentationView,
} from "../../adapters/narrativeV2PresentationAdapter";
import type { ResultNarrativeSurface } from "../../resultState/narrativeV2Shadow";
import "./narrative-v2-shadow.css";

export type NarrativeV2ShadowPageProps = {
  readonly analysis?: AnalysisDataDto | null;
  readonly mode?: Exclude<ResultNarrativeSurface, "production">;
};

const STRUCTURED_LABELS: Record<string, string> = {
  overview: "Overview",
  observation: "Observation",
  reasoning: "Reasoning",
  meaning: "Meaning",
  impact: "Impact",
  recommendation: "Recommendation",
  closing: "Closing",
};

const MISSING_REVIEW = "Không có trong Presentation";

/**
 * Developer / Product Owner shadow review of NarrativeV2Presentation v2.1.
 */
export function NarrativeV2ShadowPage({
  analysis = null,
  mode = "v2-shadow",
}: NarrativeV2ShadowPageProps): ReactNode {
  const view = adaptNarrativeV2Presentation(analysis?.narrative_v2_shadow);
  const production = adaptProductionNarrativeSnippet(analysis?.narrative_result);
  const compare = mode === "v2-compare";

  return (
    <div
      className="bte-v2s"
      data-narrative-surface={mode}
      data-narrative-v2-shadow="true"
    >
      <header className="bte-v2s__banner">
        <p className="bte-v2s__kicker">Narrative V2 — Shadow Review</p>
        <h1 className="bte-v2s__title">Xem Presentation v2.1 (không phải luồng khách hàng)</h1>
        <p className="bte-v2s__meta" data-v2-status>
          status: {view.status ?? "unavailable"} · version: {view.version ?? "rejected"} ·
          replaces_pack05: false
        </p>
        <p className="bte-v2s__links">
          <a href="/result">Về kết quả production</a>
          <a href="/result?narrative=v2-shadow">Shadow</a>
          <a href="/result?narrative=v2-compare">So sánh nội bộ</a>
        </p>
      </header>

      {compare ? (
        <section className="bte-v2s__compare" data-v2-compare>
          <article className="bte-v2s__card" data-v2-production>
            <h2>CURRENT PRODUCTION</h2>
            <p>contract: {production.contract ?? "không có"}</p>
            {production.identity ? <p>{production.identity}</p> : <p className="bte-v2s__missing">{MISSING_REVIEW}</p>}
            {production.priority ? <p>{production.priority}</p> : null}
          </article>
          <article className="bte-v2s__card" data-v2-shadow-column>
            <h2>NARRATIVE V2 SHADOW</h2>
            {view.ok ? <ShadowBody view={view} /> : <ShadowError error={view.error} />}
          </article>
        </section>
      ) : view.ok ? (
        <ShadowBody view={view} />
      ) : (
        <ShadowError error={view.error} />
      )}
    </div>
  );
}

function ShadowError({ error }: { readonly error: string | null }): ReactNode {
  return (
    <section className="bte-v2s__card" data-v2-error>
      <h2>Không tải được Narrative V2</h2>
      <p>{error ?? "presentation_unavailable"}</p>
      <p>Production /result không bị ảnh hưởng.</p>
    </section>
  );
}

function ShadowBody({ view }: { readonly view: NarrativeV2PresentationView }): ReactNode {
  return (
    <>
      <OverviewBlock overview={view.overview} />
      <InterpretationBlock interpretation={view.interpretation} />
      <ActionBlock plan={view.action_plan} />
      <section className="bte-v2s__card" data-v2-commercial>
        <h2>Commercial</h2>
        <p className="bte-v2s__missing">Chưa có (Commercial Builder chưa triển khai)</p>
      </section>
    </>
  );
}

function OverviewBlock({ overview }: { readonly overview: NarrativeV2OverviewView | null }): ReactNode {
  return (
    <section className="bte-v2s__card" data-v2-overview>
      <h2>1. Overview</h2>
      {overview?.headline ? <p data-v2-headline>{overview.headline}</p> : null}
      {overview?.summary ? <p data-v2-summary>{overview.summary}</p> : null}
      <OptionalField label="identity" value={overview?.identity ?? null} />
      <OptionalField label="balance" value={overview?.balance ?? null} />
      <OptionalField label="conclusion" value={overview?.conclusion ?? null} />
    </section>
  );
}

function InterpretationBlock({
  interpretation,
}: {
  readonly interpretation: NarrativeV2PresentationView["interpretation"];
}): ReactNode {
  const details = structuredInterpretationEntries(interpretation);
  return (
    <section className="bte-v2s__card" data-v2-interpretation>
      <h2>2. Interpretation consulting_flow</h2>
      {interpretation?.consulting_flow ? (
        <p data-v2-consulting-flow>{interpretation.consulting_flow}</p>
      ) : (
        <p className="bte-v2s__missing">{MISSING_REVIEW}</p>
      )}
      <details className="bte-v2s__details" data-v2-structured>
        <summary>3. Structured Interpretation details</summary>
        {details.map((item) => (
          <div key={item.key} data-v2-structured-field={item.key}>
            <h3>{STRUCTURED_LABELS[item.key]}</h3>
            <p>{item.text}</p>
          </div>
        ))}
      </details>
    </section>
  );
}

function ActionBlock({ plan }: { readonly plan: NarrativeV2ActionView | null }): ReactNode {
  return (
    <section className="bte-v2s__card" data-v2-action>
      <h2>4. Action Plan</h2>
      {plan?.top_priority ? (
        <div data-v2-top-priority>
          <h3>{plan.top_priority.title}</h3>
          <p>{plan.top_priority.description}</p>
        </div>
      ) : (
        <p className="bte-v2s__missing">{MISSING_REVIEW}</p>
      )}
      <ol>
        {plan?.actions.map((item) => (
          <li key={item.title} data-v2-action-item>
            <strong>{item.title}</strong>
            <p>{item.description}</p>
          </li>
        ))}
      </ol>
      {plan?.warnings.map((item) => (
        <p key={item.title} data-v2-warning>
          {item.title}: {item.description}
        </p>
      ))}
      {plan?.current_period ? (
        <p data-v2-current-period>
          {plan.current_period.title}: {plan.current_period.description}
        </p>
      ) : (
        <p className="bte-v2s__missing" data-v2-current-period-missing>
          current_period: {MISSING_REVIEW}
        </p>
      )}
    </section>
  );
}

function OptionalField({ label, value }: { readonly label: string; readonly value: string | null }): ReactNode {
  if (value) {
    return (
      <p data-v2-overview-field={label}>
        {label}: {value}
      </p>
    );
  }
  return (
    <p className="bte-v2s__missing" data-v2-overview-missing={label}>
      {label}: {MISSING_REVIEW}
    </p>
  );
}
