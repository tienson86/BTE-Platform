import { useId, useState, type ReactNode } from "react";
import { BaseStack } from "../base";
import { cx } from "../../utils";

export type TabItem = {
  id: string;
  label: ReactNode;
  content: ReactNode;
};

export type TabPanelProps = {
  items: TabItem[];
  defaultTabId?: string;
  className?: string;
};

/** Shared tabs container. Local UI state only. */
export function TabPanel({ items, defaultTabId, className }: TabPanelProps) {
  const reactId = useId();
  const [activeId, setActiveId] = useState(defaultTabId ?? items[0]?.id ?? "");
  const active = items.find((item) => item.id === activeId) ?? items[0];

  return (
    <BaseStack gap="list" className={cx("cui-shared-tab-panel", className)}>
      <div role="tablist" aria-label="Tabs" className="cui-shared-tabs__list">
        {items.map((item) => {
          const selected = item.id === active?.id;
          return (
            <button
              key={item.id}
              type="button"
              role="tab"
              id={`${reactId}-tab-${item.id}`}
              className="cui-shared-tabs__tab"
              aria-selected={selected}
              aria-controls={`${reactId}-panel-${item.id}`}
              tabIndex={selected ? 0 : -1}
              onClick={() => setActiveId(item.id)}
            >
              {item.label}
            </button>
          );
        })}
      </div>
      {active ? (
        <div
          role="tabpanel"
          id={`${reactId}-panel-${active.id}`}
          aria-labelledby={`${reactId}-tab-${active.id}`}
          className="cui-shared-tabs__panel"
        >
          {active.content}
        </div>
      ) : null}
    </BaseStack>
  );
}
