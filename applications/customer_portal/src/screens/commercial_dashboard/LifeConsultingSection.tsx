/**
 * Life Consulting section — domains first. Not a dashboard card.
 */

import type { ReactNode } from "react";
import type { LifeConsultingView, LifeDomainView } from "./types";

type LifeConsultingSectionProps = {
  readonly model: LifeConsultingView;
};

const FIELDS: readonly {
  readonly key: Exclude<keyof LifeDomainView, "id" | "title" | "insight">;
  readonly label: string;
}[] = [
  { key: "tendency", label: "Xu hướng hiện tại" },
  { key: "strength", label: "Điểm mạnh" },
  { key: "opportunity", label: "Cơ hội" },
  { key: "risk", label: "Rủi ro" },
  { key: "recommendation", label: "Hướng đi" },
];

function DomainCard({ item }: { readonly item: LifeDomainView }): ReactNode {
  return (
    <article className="bte-life__domain" data-life-domain={item.id}>
      <header className="bte-life__domain-head">
        <h3 className="bte-life__domain-title">{item.title}</h3>
      </header>
      <p className="bte-life__insight" data-life-field="insight">
        {item.insight}
      </p>
      <dl className="bte-life__fields">
        {FIELDS.map((field) => (
          <div key={field.key} data-life-field={field.key}>
            <dt>{field.label}</dt>
            <dd>{item[field.key]}</dd>
          </div>
        ))}
      </dl>
    </article>
  );
}

/**
 * Customer life-domain consulting. Renders nothing when no domain matched.
 */
export function LifeConsultingSection({ model }: LifeConsultingSectionProps): ReactNode {
  if (!model.available || !model.domains.length) return null;
  return (
    <section
      className="bte-life"
      data-life-consulting="true"
      aria-label={model.title}
    >
      <header className="bte-life__header">
        <h2 className="bte-life__title">{model.title}</h2>
      </header>
      <div className="bte-life__grid">
        {model.domains.map((item) => (
          <DomainCard key={item.id} item={item} />
        ))}
      </div>
    </section>
  );
}
