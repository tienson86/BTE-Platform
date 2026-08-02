import { useId, useState, type ReactNode } from "react";
import { BaseStack, BaseSurface } from "../base";
import { cx } from "../../utils";

export type AccordionItemData = {
  id: string;
  title: ReactNode;
  content: ReactNode;
};

export type AccordionProps = {
  items: AccordionItemData[];
  allowMultiple?: boolean;
  className?: string;
};

/** Shared accordion group. Local UI state only. */
export function Accordion({ items, allowMultiple = false, className }: AccordionProps) {
  const reactId = useId();
  const [openIds, setOpenIds] = useState<string[]>([]);

  const toggle = (id: string) => {
    setOpenIds((current) => {
      const isOpen = current.includes(id);
      if (allowMultiple) {
        return isOpen ? current.filter((item) => item !== id) : [...current, id];
      }
      return isOpen ? [] : [id];
    });
  };

  return (
    <BaseStack gap="list" className={cx(className)}>
      {items.map((item) => {
        const isOpen = openIds.includes(item.id);
        const panelId = `${reactId}-${item.id}`;
        return (
          <BaseSurface key={item.id} variant="section" className="cui-shared-accordion-item">
            <button
              type="button"
              className="cui-shared-accordion__trigger"
              aria-expanded={isOpen}
              aria-controls={panelId}
              onClick={() => toggle(item.id)}
            >
              <span>{item.title}</span>
              <span aria-hidden="true">{isOpen ? "−" : "+"}</span>
            </button>
            {isOpen ? (
              <div id={panelId} className="cui-shared-accordion__panel" role="region">
                {item.content}
              </div>
            ) : null}
          </BaseSurface>
        );
      })}
    </BaseStack>
  );
}
