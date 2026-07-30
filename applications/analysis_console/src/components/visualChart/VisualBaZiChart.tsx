import {
  useCallback,
  useId,
  useMemo,
  useState,
  type KeyboardEvent,
  type PointerEvent,
} from "react";
import {
  buildVisualBaZiModel,
  type VisualBaZiModel,
  type VisualPillar,
} from "../../bazi/buildVisualModel";
import {
  ELEMENT_COLOR,
  ELEMENT_ORDER,
  type ElementId,
  type PillarKey,
} from "../../bazi/knowledge";
import type { AnalysisData, ChartData } from "../../api/types";

type TooltipState = {
  x: number;
  y: number;
  title: string;
  lines: string[];
} | null;

type HighlightMode =
  | { type: "none" }
  | { type: "pillar"; key: PillarKey }
  | { type: "element"; element: ElementId }
  | { type: "relation"; id: string };

type VisualBaZiChartProps = {
  chart: ChartData;
  analysis?: AnalysisData | null;
};

function elementFill(element: ElementId | null): string {
  if (!element) return "var(--muted)";
  return ELEMENT_COLOR[element].fill;
}

export function VisualBaZiChart({
  chart,
  analysis = null,
}: VisualBaZiChartProps) {
  const model = useMemo(
    () => buildVisualBaZiModel(chart, analysis),
    [chart, analysis],
  );
  const reactId = useId();
  const [tooltip, setTooltip] = useState<TooltipState>(null);
  const [highlight, setHighlight] = useState<HighlightMode>({ type: "none" });
  const [pinned, setPinned] = useState<HighlightMode>({ type: "none" });

  const activeHighlight = pinned.type !== "none" ? pinned : highlight;

  const maxElement = Math.max(...ELEMENT_ORDER.map((el) => model.elements[el]), 1);

  const showTooltip = useCallback(
    (event: PointerEvent<SVGElement>, title: string, lines: string[]) => {
      const svg = event.currentTarget.ownerSVGElement;
      if (!svg) return;
      const rect = svg.getBoundingClientRect();
      setTooltip({
        x: event.clientX - rect.left,
        y: event.clientY - rect.top,
        title,
        lines,
      });
    },
    [],
  );

  const clearHover = useCallback(() => {
    setTooltip(null);
    if (pinned.type === "none") setHighlight({ type: "none" });
  }, [pinned.type]);

  const isPillarDimmed = (key: PillarKey): boolean => {
    if (activeHighlight.type === "none") return false;
    if (activeHighlight.type === "pillar") return activeHighlight.key !== key;
    if (activeHighlight.type === "element") {
      const pillar = model.pillars.find((p) => p.key === key);
      return (
        pillar?.stem_element !== activeHighlight.element &&
        pillar?.branch_element !== activeHighlight.element
      );
    }
    if (activeHighlight.type === "relation") {
      const relation = model.relations.find((r) => r.id === activeHighlight.id);
      if (!relation || relation.pillars.length === 0) return false;
      return !relation.pillars.includes(key);
    }
    return false;
  };

  const isElementDimmed = (element: ElementId): boolean => {
    if (activeHighlight.type === "element") {
      return activeHighlight.element !== element;
    }
    if (activeHighlight.type === "pillar") {
      const pillar = model.pillars.find((p) => p.key === activeHighlight.key);
      return (
        pillar?.stem_element !== element && pillar?.branch_element !== element
      );
    }
    return false;
  };

  function onPillarActivate(pillar: VisualPillar) {
    const next: HighlightMode = { type: "pillar", key: pillar.key };
    setPinned((prev) =>
      prev.type === "pillar" && prev.key === pillar.key
        ? { type: "none" }
        : next,
    );
  }

  function pillarKeyHandler(pillar: VisualPillar) {
    return (event: KeyboardEvent<SVGGElement>) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        onPillarActivate(pillar);
      }
    };
  }

  const width = 920;
  const height = 560;
  const colX = [80, 200, 320, 440];

  return (
    <div className="relative w-full overflow-hidden rounded-2xl border border-[var(--line)] bg-[var(--bg-elevated)]">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[var(--line)] px-4 py-3">
        <div>
          <h2 className="font-display text-2xl font-semibold">Visual BaZi Chart</h2>
          <p className="text-sm text-[var(--muted)]">
            SVG · hover for details · click to pin highlight · dark-mode aware
          </p>
        </div>
        <div className="flex flex-wrap gap-2 text-xs">
          <span className="rounded-full bg-[var(--accent-soft)] px-3 py-1 font-medium text-[var(--accent)]">
            Day Master {model.day_master}
          </span>
          <span className="rounded-full border border-[var(--line)] px-3 py-1 text-[var(--muted)]">
            Season {model.season}
          </span>
          <span className="rounded-full border border-[var(--line)] px-3 py-1 text-[var(--muted)]">
            Strength {model.strength}
          </span>
        </div>
      </div>

      <div className="relative w-full overflow-x-auto">
        <svg
          role="img"
          aria-labelledby={`${reactId}-title ${reactId}-desc`}
          viewBox={`0 0 ${width} ${height}`}
          className="mx-auto h-auto min-w-[640px] w-full max-w-5xl"
        >
          <title id={`${reactId}-title`}>Visual BaZi Chart</title>
          <desc id={`${reactId}-desc`}>
            Interactive four pillars chart with hidden stems, ten gods, five
            elements, strength, useful god, season, combinations, clashes, and
            luck pillars.
          </desc>

          <rect
            x={0}
            y={0}
            width={width}
            height={height}
            fill="transparent"
          />

          {/* Four pillars */}
          <text
            x={40}
            y={36}
            fill="var(--muted)"
            fontSize={12}
            fontFamily="var(--font-sans)"
          >
            Four Pillars
          </text>

          {model.pillars.map((pillar, index) => {
            const x = colX[index];
            const dimmed = isPillarDimmed(pillar.key);
            const highlighted =
              activeHighlight.type === "pillar" &&
              activeHighlight.key === pillar.key;
            return (
              <g
                key={pillar.key}
                tabIndex={0}
                role="button"
                aria-label={`${pillar.label} pillar ${pillar.stem} ${pillar.branch}`}
                aria-pressed={highlighted}
                opacity={dimmed ? 0.28 : 1}
                className="outline-none focus-visible:opacity-100"
                onKeyDown={pillarKeyHandler(pillar)}
                onClick={() => onPillarActivate(pillar)}
                onPointerEnter={(event) => {
                  setHighlight({ type: "pillar", key: pillar.key });
                  showTooltip(event, `${pillar.label} Pillar`, [
                    `Stem: ${pillar.stem} (${pillar.stem_element ?? "—"})`,
                    `Branch: ${pillar.branch} (${pillar.branch_element ?? "—"})`,
                    `Hidden: ${pillar.hidden_stems.join(", ") || "—"}`,
                    `Ten God: ${pillar.ten_god}`,
                    `Season: ${pillar.season}`,
                  ]);
                }}
                onPointerMove={(event) =>
                  showTooltip(event, `${pillar.label} Pillar`, [
                    `Stem: ${pillar.stem} (${pillar.stem_element ?? "—"})`,
                    `Branch: ${pillar.branch} (${pillar.branch_element ?? "—"})`,
                    `Hidden: ${pillar.hidden_stems.join(", ") || "—"}`,
                    `Ten God: ${pillar.ten_god}`,
                    `Season: ${pillar.season}`,
                  ])
                }
                onPointerLeave={clearHover}
                style={{ cursor: "pointer" }}
              >
                <text
                  x={x + 40}
                  y={58}
                  textAnchor="middle"
                  fill="var(--muted)"
                  fontSize={11}
                >
                  {pillar.label}
                </text>

                {/* Stem */}
                <rect
                  x={x}
                  y={70}
                  width={80}
                  height={56}
                  rx={12}
                  fill={elementFill(pillar.stem_element)}
                  stroke={highlighted ? "var(--accent)" : "var(--line)"}
                  strokeWidth={highlighted ? 3 : 1}
                />
                <text
                  x={x + 40}
                  y={95}
                  textAnchor="middle"
                  fill="#fff"
                  fontSize={18}
                  fontWeight={600}
                  fontFamily="var(--font-display)"
                >
                  {pillar.stem}
                </text>
                <text
                  x={x + 40}
                  y={114}
                  textAnchor="middle"
                  fill="rgba(255,255,255,0.85)"
                  fontSize={10}
                >
                  Stem
                </text>

                {/* Branch */}
                <rect
                  x={x}
                  y={136}
                  width={80}
                  height={56}
                  rx={12}
                  fill={elementFill(pillar.branch_element)}
                  opacity={0.92}
                  stroke={highlighted ? "var(--accent)" : "var(--line)"}
                  strokeWidth={highlighted ? 3 : 1}
                />
                <text
                  x={x + 40}
                  y={161}
                  textAnchor="middle"
                  fill="#fff"
                  fontSize={18}
                  fontWeight={600}
                  fontFamily="var(--font-display)"
                >
                  {pillar.branch}
                </text>
                <text
                  x={x + 40}
                  y={180}
                  textAnchor="middle"
                  fill="rgba(255,255,255,0.85)"
                  fontSize={10}
                >
                  Branch
                </text>

                {/* Hidden stems */}
                <text
                  x={x + 40}
                  y={214}
                  textAnchor="middle"
                  fill="var(--fg)"
                  fontSize={11}
                  fontWeight={600}
                >
                  {pillar.hidden_stems.join(" ") || "—"}
                </text>
                <text
                  x={x + 40}
                  y={230}
                  textAnchor="middle"
                  fill="var(--muted)"
                  fontSize={10}
                >
                  Hidden Stems
                </text>

                {/* Ten God */}
                <rect
                  x={x}
                  y={244}
                  width={80}
                  height={34}
                  rx={10}
                  fill="var(--accent-soft)"
                  stroke="var(--line)"
                />
                <text
                  x={x + 40}
                  y={265}
                  textAnchor="middle"
                  fill="var(--accent)"
                  fontSize={11}
                  fontWeight={600}
                >
                  {pillar.ten_god}
                </text>
              </g>
            );
          })}

          {/* Five Elements */}
          <text
            x={560}
            y={36}
            fill="var(--muted)"
            fontSize={12}
            fontFamily="var(--font-sans)"
          >
            Five Elements
          </text>
          {ELEMENT_ORDER.map((element, index) => {
            const y = 58 + index * 36;
            const value = model.elements[element];
            const barWidth = (value / maxElement) * 220;
            const dimmed = isElementDimmed(element);
            return (
              <g
                key={element}
                opacity={dimmed ? 0.28 : 1}
                tabIndex={0}
                role="button"
                aria-label={`${element} ${value}`}
                onKeyDown={(event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    setPinned((prev) =>
                      prev.type === "element" && prev.element === element
                        ? { type: "none" }
                        : { type: "element", element },
                    );
                  }
                }}
                onClick={() =>
                  setPinned((prev) =>
                    prev.type === "element" && prev.element === element
                      ? { type: "none" }
                      : { type: "element", element },
                  )
                }
                onPointerEnter={(event) => {
                  setHighlight({ type: "element", element });
                  showTooltip(event, element, [
                    `Weight: ${value}`,
                    "Click to highlight related pillars",
                  ]);
                }}
                onPointerMove={(event) =>
                  showTooltip(event, element, [
                    `Weight: ${value}`,
                    "Click to highlight related pillars",
                  ])
                }
                onPointerLeave={clearHover}
                style={{ cursor: "pointer" }}
              >
                <text x={560} y={y + 14} fill="var(--fg)" fontSize={12}>
                  {element}
                </text>
                <rect
                  x={620}
                  y={y}
                  width={220}
                  height={18}
                  rx={9}
                  fill="var(--line)"
                />
                <rect
                  x={620}
                  y={y}
                  width={Math.max(barWidth, value > 0 ? 8 : 0)}
                  height={18}
                  rx={9}
                  fill={ELEMENT_COLOR[element].fill}
                />
                <text
                  x={850}
                  y={y + 14}
                  textAnchor="end"
                  fill="var(--muted)"
                  fontSize={11}
                >
                  {value}
                </text>
              </g>
            );
          })}

          {/* Strength / Useful God / Season panel */}
          <g>
            <rect
              x={560}
              y={250}
              width={320}
              height={110}
              rx={14}
              fill="var(--bg)"
              stroke="var(--line)"
            />
            <text x={576} y={274} fill="var(--muted)" fontSize={11}>
              Strength
            </text>
            <text x={576} y={296} fill="var(--fg)" fontSize={16} fontWeight={600}>
              {model.strength}
            </text>
            <text x={576} y={322} fill="var(--muted)" fontSize={11}>
              Useful God
            </text>
            <text x={576} y={344} fill="var(--accent)" fontSize={14} fontWeight={600}>
              {model.useful_gods.length
                ? model.useful_gods.join(" · ")
                : model.analysis_available
                  ? "—"
                  : "Run analysis"}
            </text>
          </g>

          {/* Relations */}
          <text x={40} y={310} fill="var(--muted)" fontSize={12}>
            Combinations & Clashes
          </text>
          {model.relations.length === 0 ? (
            <text x={40} y={334} fill="var(--fg)" fontSize={13}>
              No clash/combination signals detected
            </text>
          ) : (
            model.relations.slice(0, 4).map((relation, index) => {
              const y = 330 + index * 28;
              const active =
                activeHighlight.type === "relation" &&
                activeHighlight.id === relation.id;
              return (
                <g
                  key={relation.id}
                  tabIndex={0}
                  role="button"
                  aria-label={relation.label}
                  onClick={() =>
                    setPinned((prev) =>
                      prev.type === "relation" && prev.id === relation.id
                        ? { type: "none" }
                        : { type: "relation", id: relation.id },
                    )
                  }
                  onKeyDown={(event) => {
                    if (event.key === "Enter" || event.key === " ") {
                      event.preventDefault();
                      setPinned((prev) =>
                        prev.type === "relation" && prev.id === relation.id
                          ? { type: "none" }
                          : { type: "relation", id: relation.id },
                      );
                    }
                  }}
                  onPointerEnter={(event) => {
                    setHighlight({ type: "relation", id: relation.id });
                    showTooltip(event, relation.kind, [relation.label]);
                  }}
                  onPointerLeave={clearHover}
                  style={{ cursor: "pointer" }}
                >
                  <rect
                    x={40}
                    y={y - 14}
                    width={480}
                    height={24}
                    rx={8}
                    fill={active ? "var(--accent-soft)" : "transparent"}
                    stroke={active ? "var(--accent)" : "var(--line)"}
                  />
                  <circle
                    cx={54}
                    cy={y - 2}
                    r={5}
                    fill={
                      relation.kind === "clash"
                        ? "var(--danger)"
                        : "var(--accent)"
                    }
                  />
                  <text x={68} y={y + 2} fill="var(--fg)" fontSize={12}>
                    {relation.label}
                  </text>
                </g>
              );
            })
          )}

          {/* Luck pillars */}
          <text x={40} y={460} fill="var(--muted)" fontSize={12}>
            Luck Pillars (Da Yun)
          </text>
          {model.luck_pillars.length === 0 ? (
            <text x={40} y={488} fill="var(--fg)" fontSize={13}>
              No luck pillars on chart
            </text>
          ) : (
            model.luck_pillars.map((luck, index) => {
              const x = 40 + index * 120;
              return (
                <g
                  key={luck.id}
                  onPointerEnter={(event) =>
                    showTooltip(event, luck.label, [
                      `${luck.stem} ${luck.branch}`,
                      luck.meta,
                      luck.active ? "Active" : "Inactive",
                    ])
                  }
                  onPointerLeave={clearHover}
                >
                  <rect
                    x={x}
                    y={472}
                    width={108}
                    height={64}
                    rx={12}
                    fill={
                      luck.active ? "var(--accent-soft)" : "var(--bg)"
                    }
                    stroke={luck.active ? "var(--accent)" : "var(--line)"}
                    strokeWidth={luck.active ? 2 : 1}
                  />
                  <text
                    x={x + 54}
                    y={494}
                    textAnchor="middle"
                    fill="var(--muted)"
                    fontSize={10}
                  >
                    {luck.label}
                  </text>
                  <text
                    x={x + 54}
                    y={516}
                    textAnchor="middle"
                    fill={elementFill(luck.stem_element)}
                    fontSize={14}
                    fontWeight={700}
                  >
                    {luck.stem} {luck.branch}
                  </text>
                </g>
              );
            })
          )}
        </svg>

        {tooltip ? (
          <div
            role="tooltip"
            className="pointer-events-none absolute z-10 max-w-xs rounded-xl border border-[var(--line)] bg-[var(--bg)] px-3 py-2 text-xs shadow-[var(--shadow)]"
            style={{
              left: Math.min(tooltip.x + 12, 640),
              top: Math.max(tooltip.y - 12, 8),
            }}
          >
            <p className="font-semibold text-[var(--fg)]">{tooltip.title}</p>
            <ul className="mt-1 space-y-0.5 text-[var(--muted)]">
              {tooltip.lines.map((line) => (
                <li key={line}>{line}</li>
              ))}
            </ul>
          </div>
        ) : null}
      </div>

      <Legend model={model} />
    </div>
  );
}

function Legend({ model }: { model: VisualBaZiModel }) {
  return (
    <div className="flex flex-wrap gap-3 border-t border-[var(--line)] px-4 py-3 text-xs text-[var(--muted)]">
      {ELEMENT_ORDER.map((element) => (
        <span key={element} className="inline-flex items-center gap-1.5">
          <span
            className="inline-block h-2.5 w-2.5 rounded-full"
            style={{ background: ELEMENT_COLOR[element].fill }}
            aria-hidden
          />
          {element}
        </span>
      ))}
      <span className="ml-auto">
        {model.analysis_available
          ? "Analysis overlays active"
          : "Chart-only mode · run analysis for strength & useful god"}
      </span>
    </div>
  );
}
