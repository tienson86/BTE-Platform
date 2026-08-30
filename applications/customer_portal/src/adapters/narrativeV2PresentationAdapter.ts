/**
 * NarrativeV2Presentation v2.1 adapter.
 * Copies Presentation fields only. Does not compose or rewrite Narrative.
 */

export const PRESENTATION_V2_1 = "bte.presentation.v2.1";

const STRUCTURED_KEYS = [
  "overview",
  "observation",
  "reasoning",
  "meaning",
  "impact",
  "recommendation",
  "closing",
] as const;

export type StructuredInterpretationKey = (typeof STRUCTURED_KEYS)[number];

export type NarrativeV2OverviewView = {
  readonly headline: string | null;
  readonly summary: string | null;
  readonly identity: string | null;
  readonly balance: string | null;
  readonly conclusion: string | null;
};

export type NarrativeV2InterpretationView = {
  readonly consulting_flow: string | null;
  readonly overview: string | null;
  readonly observation: string | null;
  readonly reasoning: string | null;
  readonly meaning: string | null;
  readonly impact: string | null;
  readonly recommendation: string | null;
  readonly closing: string | null;
};

export type NarrativeV2ActionItemView = {
  readonly title: string;
  readonly description: string;
  readonly category: string;
};

export type NarrativeV2ActionView = {
  readonly top_priority: { readonly title: string; readonly description: string } | null;
  readonly actions: readonly NarrativeV2ActionItemView[];
  readonly warnings: readonly { readonly title: string; readonly description: string }[];
  readonly current_period: { readonly title: string; readonly description: string } | null;
};

export type NarrativeV2PresentationView = {
  readonly ok: boolean;
  readonly error: string | null;
  readonly version: string | null;
  readonly status: string | null;
  readonly language: string | null;
  readonly overview: NarrativeV2OverviewView | null;
  readonly interpretation: NarrativeV2InterpretationView | null;
  readonly action_plan: NarrativeV2ActionView | null;
  readonly commercial: null;
};

export type ProductionNarrativeSnippet = {
  readonly contract: string | null;
  readonly identity: string | null;
  readonly priority: string | null;
};

/**
 * Adapt the stored shadow envelope into a render view. Rejects incompatible versions.
 */
export function adaptNarrativeV2Presentation(envelope: unknown): NarrativeV2PresentationView {
  const record = asRecord(envelope);
  if (!record) {
    return failed("shadow_envelope_missing");
  }
  if (record.status === "error" || record.presentation == null) {
    return failed(asText(record.error) ?? "presentation_unavailable");
  }
  const presentation = asRecord(record.presentation);
  if (!presentation) {
    return failed("presentation_unavailable");
  }
  const metadata = asRecord(presentation.metadata);
  const version = asText(metadata?.version);
  if (version !== PRESENTATION_V2_1) {
    return failed("incompatible_presentation_version");
  }
  return {
    ok: true,
    error: null,
    version,
    status: asText(presentation.status) ?? asText(metadata?.status),
    language: asText(metadata?.language),
    overview: copyOverview(asRecord(presentation.overview)),
    interpretation: copyInterpretation(asRecord(presentation.interpretation)),
    action_plan: copyActionPlan(asRecord(presentation.action_plan)),
    commercial: null,
  };
}

/**
 * Copy Pack05 snippets for comparison only. Does not build Narrative V2.
 */
export function adaptProductionNarrativeSnippet(narrativeResult: unknown): ProductionNarrativeSnippet {
  const record = asRecord(narrativeResult);
  const summary = asRecord(record?.summary);
  return {
    contract: asText(record?.contract),
    identity: asText(summary?.identity),
    priority: asText(summary?.priority_recommendation),
  };
}

export function structuredInterpretationEntries(
  interpretation: NarrativeV2InterpretationView | null,
): readonly { readonly key: StructuredInterpretationKey; readonly text: string }[] {
  if (!interpretation) return [];
  return STRUCTURED_KEYS.flatMap((key) => {
    const text = interpretation[key];
    return text ? [{ key, text }] : [];
  });
}

function copyOverview(value: Record<string, unknown> | null): NarrativeV2OverviewView | null {
  if (!value) return null;
  return {
    headline: asText(value.headline),
    summary: asText(value.summary),
    identity: asText(value.identity),
    balance: asText(value.balance),
    conclusion: asText(value.conclusion),
  };
}

function copyInterpretation(value: Record<string, unknown> | null): NarrativeV2InterpretationView | null {
  if (!value) return null;
  return {
    consulting_flow: asText(value.consulting_flow),
    overview: asText(value.overview),
    observation: asText(value.observation),
    reasoning: asText(value.reasoning),
    meaning: asText(value.meaning),
    impact: asText(value.impact),
    recommendation: asText(value.recommendation),
    closing: asText(value.closing),
  };
}

function copyActionPlan(value: Record<string, unknown> | null): NarrativeV2ActionView | null {
  if (!value) return null;
  const top = asRecord(value.top_priority);
  const period = asRecord(value.current_period);
  return {
    top_priority: top
      ? { title: asText(top.title) ?? "", description: asText(top.description) ?? "" }
      : null,
    actions: asList(value.actions).flatMap((item) => {
      const row = asRecord(item);
      if (!row) return [];
      return [
        {
          title: asText(row.title) ?? "",
          description: asText(row.description) ?? "",
          category: asText(row.category) ?? "",
        },
      ];
    }),
    warnings: asList(value.warnings).flatMap((item) => {
      const row = asRecord(item);
      if (!row) return [];
      return [{ title: asText(row.title) ?? "", description: asText(row.description) ?? "" }];
    }),
    current_period: period
      ? { title: asText(period.title) ?? "", description: asText(period.description) ?? "" }
      : null,
  };
}

function failed(error: string): NarrativeV2PresentationView {
  return {
    ok: false,
    error,
    version: null,
    status: null,
    language: null,
    overview: null,
    interpretation: null,
    action_plan: null,
    commercial: null,
  };
}

function asRecord(value: unknown): Record<string, unknown> | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  return value as Record<string, unknown>;
}

function asList(value: unknown): readonly unknown[] {
  return Array.isArray(value) ? value : [];
}

function asText(value: unknown): string | null {
  if (typeof value !== "string") return null;
  const trimmed = value.trim();
  return trimmed ? value : null;
}
